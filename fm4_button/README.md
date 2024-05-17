# FM4 Button Service

This service is designed to run on a Raspberry Pi and fetches the current song playing on the FM4 radio station. It also includes GPIO event handling to reset the program state via a button press.

## Service Details

- **Service Name:** `fm4`
- **Description:** This service continuously runs and fetches the current song from the FM4 radio station. It also supports GPIO button inputs for resetting the program state.

## Service Setup

### Service File Configuration

1. **Create the service file:**

   ```bash
   sudo nano /etc/systemd/system/fm4.service
   ```

2. **Add the following content:**

   ```ini
   [Unit]
   Description=FM4 Button Service
   After=network.target

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your_script.py
   WorkingDirectory=/path/to/directory/containing/your_script
   Restart=always
   RestartSec=3
   StandardOutput=null
   StandardError=null

   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload systemd to apply changes:**

   ```bash
   sudo systemctl daemon-reload
   ```

4. **Start the service:**

   ```bash
   sudo systemctl start fm4
   ```

5. **Enable the service to start on boot:**

   ```bash
   sudo systemctl enable fm4
   ```

### Managing the Service

- **Restart the service:**

  ```bash
  sudo systemctl restart fm4
  ```

- **Stop the service:**

  ```bash
  sudo systemctl stop fm4
  ```

- **Disable the service:**

  ```bash
  sudo systemctl disable fm4
  ```

### Viewing Logs

By default, logging to standard output and error is disabled (redirected to `/dev/null`). However, you can view the logs if you change the logging configuration:

- **View the logs:**

  ```bash
  journalctl -u fm4
  ```

### Clearing Logs

To clear the logs periodically, set up a cron job:

1. **Edit the cron tab:**

   ```bash
   sudo crontab -e
   ```

2. **Add a job to clear logs every day at midnight:**

   ```crontab
   0 0 * * * /usr/bin/journalctl --vacuum-time=1d
   ```

## Python Script Overview

This service script fetches the current song playing on FM4 and handles GPIO inputs to reset the program state.

### Function to Fetch Current Song

```python
def get_current_song():
    url = "https://onlineradiobox.com/at/fm4/playlist/?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    song = soup.find("td", class_="track_history_item")
    return song.text.strip() if song else "Unknown"
```

Ensure you have the required Python modules installed:

```bash
pip3 install requests beautifulsoup4 rpi_lcd
```

## Additional Notes

- **GPIO Pins:** Ensure you have connected the buttons to the correct GPIO pins (11 for the main function and 13 for resetting).
- **Dependencies:** Make sure you have the necessary libraries (`requests`, `beautifulsoup4`, `RPi.GPIO`, `rpi_lcd`) installed on your Raspberry Pi.
- **Service Execution:** This service script is designed to run continuously and handle button presses to reset its state.

This README provides all the necessary details to start, manage, and understand the functionality of the `fm4` service.