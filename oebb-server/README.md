# Oebb Server

Start this server with node to get the server running. It provides the information about the next 3 trains from linz to vienna.

## Development

### Install

Node is neccessary and included in the infomenu conda environment.

```bash
npm install
```

### Run

```bash
node hello-hafas.js
```

It should run by default on localhost with port 2999

### Use

Send a GET Request to get the next the desired information.

## Raspberry

### Service

```ini
[Unit]
Description=Oebb Server
After=multi-user.target

[Service]
ExecStart=/usr/bin/node /home/janikmoller/Documents/oebb-server/hello-hafas.js
Restart=always
RestartSec=3
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=oebbserver
WorkingDirectory=/home/janikmoller/Documents/oebb-server
Environment= "PYTHONUNBUFFERED=TRUE"


[Install]
WantedBy=multi-user.target
```