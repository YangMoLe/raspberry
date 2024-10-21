# Infomenu

## Development

### Installation

Install python with env.yml

```bash
conda env create -f env.yml
```

### Use

You can just use their main function.

### Run

Run infomenu.py or other files with python

### Test

No tests

## Raspberry

### Create a service

```bash
sudo vi /etc/systemd/system/ <service-name>
```

### Service

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

### General Logs

```bash
journalctl -u infomenu| tail -n 500
```

### General Start Stop Service

```bash
sudo systemctl stop infomenu
sudo systemctl start infomenu
sudo systemctl enable infomenu
```

## Raspberry Wiring

[GPIO and the 40-pin header](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio)

| PIN | Meaning | Connected to |
| -------- | ------- | ------- |
| 11 | GPIO 17 | Button |
| February | $80 | |
| March | $420 | |

### Analog Digital Converter

### LCD
