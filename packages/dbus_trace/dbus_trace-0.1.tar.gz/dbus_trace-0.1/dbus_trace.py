"""Inspect the D-Bus messages a program sends and receives"""
import itertools
import os
import stat
import sys
import tempfile
from functools import partial
from pprint import pformat
from textwrap import indent

sys.excepthook = sys.__excepthook__  # Reset so Trio can set its except hook

import trio

from jeepney import FileDescriptor, HeaderFields, Message, MessageFlag, Parser
from jeepney.auth import Authenticator, AuthenticationError
from jeepney.bus import get_bus

__version__ = "0.1"


async def listen_unix(path: str) -> trio.SocketListener:
    sock = trio.socket.socket(family=trio.socket.AF_UNIX)
    await sock.bind(path)
    sock.listen()
    return trio.SocketListener(sock)

async def forward(src: trio.SocketStream, sink: trio.SocketStream):
    while True:
        # Buffer sizes are kind of a guess, but ancillary data (FDs) is normally
        # much smaller than the main data, so equal size is conservative.
        data, ancdata, flags, _ = await src.socket.recvmsg(
            4096, trio.socket.CMSG_SPACE(4096)
        )
        if not data:
            await sink.send_eof()
            return

        if flags & getattr(trio.socket, 'MSG_CTRUNC', 0):
            raise RuntimeError("Unable to receive all ancillary data")

        yield data, FileDescriptor.from_ancdata(ancdata)

        with memoryview(data) as data:
            # print("sendmsg", data.obj)
            try:
                bytes_sent = await sink.socket.sendmsg([data], ancdata)
                if bytes_sent < len(data):
                    await sink.send_all(data[bytes_sent:])
            except BrokenPipeError:
                return

def print_msg(msg: Message, arrow, conn_nr):
    # Avoid clutter in the common case of just 1 D-Bus connection, but allow
    # multiple connections to be distinguished.
    if conn_nr == 0:
        conn_nr = ''
        indt = '  '
    else:
        conn_nr = f' {conn_nr}'
        indt = '    '

    h = msg.header
    member = h.fields.pop(HeaderFields.member, '')
    sig = h.fields.pop(HeaderFields.signature, '')
    print(f"{arrow}{conn_nr} {h.message_type.name}: {member} [serial = {h.serial}]")
    if h.flags != 0:
        flag_names = [f.name for f in MessageFlag if (f.value & h.flags)]
        print(f"{indt}Flags: {h.flags.value} ({' | '.join(flag_names)})")
    for field, value in h.fields.items():
        print(f"{indt}{field.name} = {value}")
    if sig:
        body_str = pformat(msg.body)
        if '\n' in body_str:
            body_str = '(\n' + indent(' ' + body_str[1:-1], '      ') + ',\n    )'
            #body_str = '\n' + indent(body_str, '    ')
        print(f"{indt}Data ({sig}): {body_str}")
    print()

class Forwarder:
    def __init__(self, upstream, downstream, conn_nr):
        self.upstream = upstream
        self.downstream = downstream
        self.conn_nr = conn_nr
        self.auth_state = None  # True: succeeded, False: failed

    async def forward_down(self):
        auther = Authenticator()
        forwarding = forward(self.upstream, self.downstream)
        async for data, _ in forwarding:
            try:
                auther.feed(data)
            except AuthenticationError as e:
                pass
            if self.auth_state:
                break

        parser = Parser()
        parser.add_data(auther.buffer)
        async for data, fds in forwarding:
            parser.add_data(data, fds)
            while (msg := parser.get_next_message()) is not None:
                print_msg(msg, '▷', self.conn_nr)

    async def forward_up(self):
        forwarding = forward(self.downstream, self.upstream)
        auth_buffer = bytearray()
        async for data, _ in forwarding:
            auth_buffer += data
            if b'\r\n' in auth_buffer:
                line, auth_buffer = auth_buffer.split(b'\r\n', 1)
                if line.strip() == b'BEGIN':
                    self.auth_state = True
                    break  # Auth completed

        parser = Parser()
        parser.add_data(auth_buffer)
        async for data, fds in forwarding:
            parser.add_data(data, fds)
            while (msg := parser.get_next_message()) is not None:
                print_msg(msg, '◀', self.conn_nr)

conn_ctr = itertools.count()

async def serve_connection(upstream_path, bus, stream):
    conn_nr = next(conn_ctr)
    print(f"* Connected to {bus} bus (connection {conn_nr})")
    upstream = await trio.open_unix_socket(upstream_path)
    fwdr = Forwarder(upstream, stream, conn_nr)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(fwdr.forward_down)
        nursery.start_soon(fwdr.forward_up)
    print(f"× Connection {conn_nr} closed")

#async def serve_listener(listener, upstream_path):

async def amain():
    real_system_bus = get_bus('SYSTEM')
    if not real_system_bus.startswith('\0'):
        assert stat.S_ISSOCK(os.stat(real_system_bus).st_mode)

    real_session_bus = get_bus('SESSION')
    if not real_session_bus.startswith('\0'):
        assert stat.S_ISSOCK(os.stat(real_session_bus).st_mode)

    with tempfile.TemporaryDirectory(prefix='dbus-trace-') as td:
        proxy_system_bus = os.path.join(td, 'system_bus')
        proxy_session_bus = os.path.join(td, 'session_bus')
        system_sock_listener = await listen_unix(proxy_system_bus)
        session_sock_listener = await listen_unix(proxy_session_bus)

        async with trio.open_nursery() as nursery:
            await nursery.start(
                trio.serve_listeners,
                partial(serve_connection, real_system_bus, 'system'),
                [system_sock_listener],
            )
            await nursery.start(
                trio.serve_listeners,
                partial(serve_connection, real_session_bus, 'session'),
                [session_sock_listener],
            )
            env = os.environ.copy()
            env['DBUS_SESSION_BUS_ADDRESS'] = f'unix:path={proxy_session_bus}'
            env['DBUS_SYSTEM_BUS_ADDRESS'] = f'unix:path={proxy_system_bus}'

            res = await trio.run_process(sys.argv[1:], check=False, env=env)
            nursery.cancel_scope.cancel()
            return res.returncode

def main():
    return trio.run(amain)

if __name__ == '__main__':
    sys.exit(main())
