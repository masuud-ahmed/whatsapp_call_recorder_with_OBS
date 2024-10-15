import websocket
import json
import pygetwindow as gw
import time
import os
import threading
import obsws_python as obs

# WebSocket server address (adjust if OBS is remote)
ws_url = "ws://127.0.0.1:4444"  # Default OBS WebSocket 5.x URL and port

# Global variable to manage recording state
is_recording = False
ws_connected = False

# Event triggered when a message is received from OBS
def on_message(ws, message):
    global is_recording
    response = json.loads(message)
    print("++Rcv decoded:", response)

    # Check if the message is a response to a request
    if response.get("op") == 7:  # Handle RPC response
        data = response["d"]
        if "requestId" in data:
            if data["requestId"] == "start":
                print("OBS Recording Started")
                is_recording = True
            elif data["requestId"] == "stop":
                print("OBS Recording Stopped")
                is_recording = False

    # Check for successful identification
    if response.get('op') == 2:
        print("Identified successfully, you can now send requests")

# Event triggered when there is an error
def on_error(ws, error):
    print(f"WebSocket Error: {error}")

# Event triggered when the connection is closed
def on_close(ws, close_status_code, close_msg):
    global ws_connected
    ws_connected = False
    print(f"WebSocket connection closed. Status: {close_status_code}, Message: {close_msg}")

# Event triggered when the connection is opened
def on_open(ws):
    global ws_connected
    ws_connected = True
    print("WebSocket connection opened")

    # Send identification message after opening the connection
    identify_payload = {
        "op": 1,
        "d": {
            "rpcVersion": 1,  # The RPC version for OBS WebSocket 5.x
            # If authentication is enabled, you'll need to include the 'authentication' field
        }
    }
    ws.send(json.dumps(identify_payload))
    print("Identification message sent")

# Function to start OBS recording via WebSocket
def start_recording(ws):
    if ws_connected and not is_recording:
        start_payload = json.dumps({
            "op": 6,  # RPC request operation code
            "d": {
                "requestType": "StartRecording",
                "requestId": "start",
                # Add any additional parameters required by your OBS WebSocket version
                "requestData": {}
            }
        })
        ws.send(start_payload)

# Function to stop OBS recording via WebSocket
def stop_recording(ws):
    if ws_connected and is_recording:
        stop_payload = json.dumps({
            "op": 6,  # RPC request operation code
            "d": {
                "requestType": "StopRecording",
                "requestId": "stop",
                # Add any additional parameters required by your OBS WebSocket version
                "requestData": {}
            }
        })
        ws.send(stop_payload)

# Function to detect WhatsApp call window
def is_whatsapp_call_window_active():
    windows = gw.getWindowsWithTitle('WhatsApp')
    for window in windows:
        # Add logic to detect specific "call" elements in the window title
        if 'WhatsApp' in window.title and ('call' in window.title.lower() or 'end-to-end' in window.title.lower()):
            return True
    return False

# Main function to check for WhatsApp call status and trigger OBS
def main():
    global ws_connected 

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Start WebSocket connection in a separate thread
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

    # Wait for WebSocket to connect
    while not ws_connected:
        print("Waiting for WebSocket connection...")
        time.sleep(1)

    try:
        while True:
            if is_whatsapp_call_window_active():
                print("WhatsApp call detected")
                start_recording(ws)
            else:
                print("No active WhatsApp call")
                stop_recording(ws)
            time.sleep(5)  # Adjust the interval as needed
    except KeyboardInterrupt:
        stop_recording(ws)

if __name__ == "__main__":
    main()
