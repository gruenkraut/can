# can
Läuft auf keller01

/lib/systemd/system/

```
[Unit]
Description=mqtt2can
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/scripts/can/mqtt2can.py can0
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

und
```
[Unit]
Description=can2mqtt
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /opt/scripts/can/can2mqtt.py can0
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
