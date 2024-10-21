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
| 1 | 3V3 (True) | Plus on circuit |
| 2 | 5V Power | VDD from ADC |
| 3 | SDA | SDA (ADC, LCD) |
| 4  | 5V Power | VCC from LCD |
| 5 | SCL | SCL (ADC, LCD) |
| 6 | GND | GND from LCD |
| 11 | GPIO 17 | Button |
| 34 | GND | Ground from POTI, ADDR from ADC |

### Analog Digital Converter + Poti

```python
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance
value = adc.read_adc(0, gain=GAIN)
```

- 16Bit 12C ADC "ADS1115"
- Potentiometer

The value of the potentiometer is read by the ADCs A0 port. The other two pins from the poti are connected to 3V3 and GND.

### LCD

```python
from rpi_lcd import LCD
lcd = LCD()
```

- 1602 LCD
- I2C

Using the I2C its easy to connect to the display.

### Button

If the button is pressed the gpio pin reads a high value
