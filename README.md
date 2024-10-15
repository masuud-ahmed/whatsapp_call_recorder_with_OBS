# WhatsApp Call Recording Automation with OBS WebSocket

This project automates recording WhatsApp calls using OBS (Open Broadcaster Software) through the OBS WebSocket API. It detects when a WhatsApp call is active and starts or stops OBS recording accordingly.

## Features

- Automatically starts recording in OBS when a WhatsApp call is detected.
- Automatically stops recording when the call ends.
- Uses WebSocket to communicate with OBS.
- Detects the WhatsApp call window using `pygetwindow`.

## Requirements

### Software

- **OBS Studio**: Make sure you have OBS Studio installed. You can download it from [OBS Project](https://obsproject.com/).
- **OBS WebSocket Plugin**: This code uses the OBS WebSocket API. Download and install the OBS WebSocket plugin from [obs-websocket](https://github.com/Palakis/obs-websocket).

### Python Packages

The following Python packages are required. You can install them via `pip` using the commands provided:

- **websocket-client**: For communicating with the OBS WebSocket API.
  ```bash
  pip install websocket-client
  ```

- **pygetwindow**: To detect the WhatsApp call window on the desktop.
  ```bash
  pip install pygetwindow
  ```

- **pyautogui**: To simulate the automation of certain UI interactions if needed.
  ```bash
  pip install pyautogui
  ```

- **websockets**: For handling WebSocket connections (alternative to websocket-client, if needed).
  ```bash
  pip install websockets
  ```

- **asyncio**: For asynchronous WebSocket handling (if using asynchronous WebSocket communication).
  ```bash
  pip install asyncio
  ```

### OBS Configuration

- Ensure the OBS WebSocket server is running on port 4444 (default). You can adjust the port in the OBS WebSocket settings.
- Enable WebSocket communication in OBS by enabling the WebSocket Server (Tools -> WebSocket Server Settings).

## Setup

1. **Clone the repository**:
   Clone the project repository from GitHub to your local machine:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```

2. **Install dependencies**:
   Install the required Python libraries using the following command:
   ```bash
   pip install -r requirements.txt
   ```
   Or you can manually install each package as shown in the requirements section above.

3. **OBS WebSocket**:
   Ensure that the OBS WebSocket server is running. You can verify this in the OBS settings.

4. **Run the Script**:
   To start the script, run:
   ```bash
   python your_script.py
   ```
   The script will connect to OBS and start monitoring for WhatsApp calls. When a call is detected, recording will automatically start, and it will stop when the call ends.

## How the Code Works (Step by Step)

Here’s a detailed breakdown of how the code works step by step:

### Step 1: Connecting to OBS WebSocket
The script first establishes a connection with OBS using the `websocket-client` package. The connection is made through the WebSocket API running on port 4444 of OBS (default port).
```python
ws = websocket.WebSocket()
ws.connect("ws://localhost:4444")
```

### Step 2: Detecting WhatsApp Call Window
The script uses `pygetwindow` to monitor whether a WhatsApp call window is open and active. The function `is_whatsapp_call_window_active` continuously checks if the WhatsApp call window is in the foreground.
```python
whatsapp_window = pygetwindow.getWindowsWithTitle("WhatsApp")
if whatsapp_window and whatsapp_window.isActive:
    # WhatsApp call detected
```

### Step 3: Start Recording in OBS
When the script detects that a WhatsApp call is in progress, it sends a request to OBS to start recording. The `websocket-client` package is used to send this command to OBS over the WebSocket connection.
```python
def start_recording():
    message = '{"request-type": "StartRecording", "message-id": "start"}'
    ws.send(message)
```

### Step 4: Stop Recording in OBS
Once the WhatsApp call ends, the script sends a command to OBS to stop the recording. The function continuously checks if the call window is no longer active and then stops the recording.
```python
def stop_recording():
    message = '{"request-type": "StopRecording", "message-id": "stop"}'
    ws.send(message)
```

### Step 5: Monitoring Loop
The script runs in a loop, continuously checking the status of the WhatsApp call window. If a call is detected, it starts recording; otherwise, it stops.
```python
while True:
    if is_whatsapp_call_window_active():
        start_recording()
    else:
        stop_recording()
    time.sleep(1)  # Add a small delay between checks
```

## Troubleshooting

1. **OBS Not Recording**:
   - Ensure the WebSocket server is enabled in OBS and running on the correct port (default: 4444).
   - Ensure you have the correct WebSocket plugin version installed for your version of OBS.

2. **Recording Does Not Start/Stop**:
   - Ensure that the WhatsApp window title is being detected correctly by `pygetwindow`. If the title changes, adjust the script to match the window title.
   - Check if there are any WebSocket connection issues between the script and OBS.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Example requirements.txt
```txt
websocket-client
pygetwindow
pyautogui
websockets
asyncio
```
```

