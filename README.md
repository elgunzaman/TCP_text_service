# TCP_text_service

# Application
There are two modes in the application.
1) Change text: The client sends the text and json file and the server should swap the words from text according to json file.
2) Encode text: The client sends the text file and key file. The server must XOR the message using One Time Pad and return the encoded file to the client. 

## Installation

The code can be installed by the following command:

```bash
git clone https://github.com/elgunzaman/TCP_text_service.git
```

## Usage
Two console windows should be opened(one for server, another for client)

First console:
```bash
python text_service.py server --hostname
```
You can use "" for hostname to bind any host. Port number will be 1060 by default.

Second console:
```bash
python text_service.py client "127.0.0.1" --mode change_ text first_file.txt json_file.json
```
OR

```bash
python text_service.py client "127.0.0.1" --mode encode_text first_file.txt key.txt
```
Instead of "127.0.0.1" , you can use any host to connect. Again port number will be 1060 by default.


