# Mini-Socket
Socket Assignment done in Cosc264 at the University of Canterbury. 

This socket assignment was to create two python files:
Server creates a server in which a client can call and access the date or time in English, Te reo Maori or German.
Client accesses said server and sends a request packet (ByteArray) to get the date or time in English, Te reo Maori or German.

To run the code on a linux machine in one terminal put python3 Server.py x y z
where x, y and z are integers between 1,024 and 64,000 and all different.
To connect to the server a default IP host is defined as 127.0.0.1 so in another terminal put python3 Client.py str 127.0.0.1 a.
Where str is "date" or "time" (without quotation marks), and a is your selected port from the server (as above x is English, y is Te reo Maori and z is German)
The result is a deconstruction of the packet and a textual representation of the date/time in the selected language.
