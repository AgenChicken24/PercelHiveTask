# Percel Hive Task

## Installation
To install the necessary Python requirements for this project, run the following command:
```
pip install -r requirements.txt
```

## Configuration
The configuration settings for the web server host, web server port, websocket host, and websocket port can be found in the `config.ini` file. By default, the settings are as follows:
- Web Server Host: localhost
- Web Server Port: 9999
- Websocket Host: localhost
- Websocket Port: 8766

## Usage
1. Run the script.
2. The script will prompt you to select a camera to use.
3. After selecting the camera, the script will start the web server and websocket.
4. To save an image and its data to the `data.db` SQLite database, click the left mouse button.

## Web Server and Websocket Connection
- When you load the web server from your browser, it will automatically connect to the websocket.
- The web server will display the received data from the websocket in real-time.

## Note
Make sure to configure the `config.ini` file according to your requirements before running the script.