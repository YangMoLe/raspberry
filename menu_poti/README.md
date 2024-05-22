
```bash
sudo systemctl stop infomenu
sudo systemctl start infomenu
sudo systemctl enable infomenu

journalctl -u infomenu| tail -n 500
```


```ini
[Unit]
Description=Kitchen Info Menu Service
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3.9 /home/janikmoller/Documents/infomenu.py
Restart=always
RestartSec=3
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=infomenu
WorkingDirectory=/home/janikmoller/Documents/
Environment= "PYTHONUNBUFFERED=TRUE"


[Install]
WantedBy=multi-user.target
```


Ensure you have the required Python modules installed:

```bash
pip3 install requests beautifulsoup4 rpi_lcd
```

## Additional Notes

tbd wiring info



[Unit]
Description=Oebb Server
After=multi-user.target

[Service]
ExecStart=/usr/bin/node /home/janikmoller/Documents/oebb-server/hello-jafas.py
Restart=always
RestartSec=3
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=oebbserver
WorkingDirectory=/home/janikmoller/Documents/oebb-server
Environment= "PYTHONUNBUFFERED=TRUE"


[Install]
WantedBy=multi-user.target
