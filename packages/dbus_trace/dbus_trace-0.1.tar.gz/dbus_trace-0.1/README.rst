dbus-trace is a wrapper to see what D-Bus messages a program sends and receives.

Installation::

    pip install dbus-trace

Usage::

    dbus-trace <command>

.. code-block:: shell-session

    # For example - notify-send creates a desktop notification using D-Bus
    $ dbus-trace notify-send "Hello world"

    * Connected to session bus (connection 0)
    ◀ method_call: Hello [serial = 1]
      path = /org/freedesktop/DBus
      interface = org.freedesktop.DBus
      destination = org.freedesktop.DBus

    ...

    ◀ method_call: Notify [serial = 7]
      path = /org/freedesktop/Notifications
      interface = org.freedesktop.Notifications
      destination = :1.44
      Data (susssasa{sv}i): (
           'notify-send',
           0,
           '',
           'Hello world',
           '',
           [],
           {'sender-pid': ('x', 31559), 'urgency': ('y', 1)},
           -1,
        )

    ▷ method_return:  [serial = 88]
      Flags: 1 (no_reply_expected)
      destination = :1.944
      reply_serial = 7
      sender = :1.44
      Data (u): (8,)

    ...

dbus-trace listens on Unix sockets for the system bus and the session bus, and
passes through any data sent to these sockets to the real buses. It runs the
child program with environment variables pointing it to use these proxy sockets,
and of course it decodes what's going through and prints it to the terminal.

For more background about D-Bus, see `What is D-Bus? <https://jeepney.readthedocs.io/en/latest/dbus-background.html>`_.
