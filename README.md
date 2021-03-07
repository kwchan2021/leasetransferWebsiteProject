# Simplified IRC
provide a chatting service for the clients connecting to the server with a server console that monitors the whole process.

- client application
client(s) can join the server after running the app in terminal
Those who joined to the server(s) running will be added to the #global channel automatically
And those who joined the server with the same ip address and port will be able to see messages from others who also joined the same server

- server application
a console to update all the activities of the IRC (e.g. messages sent from clients, join/quit of clients)

- to optimize the IRC
follows closely to RFC1459

- design pattern
follows closely to the observer design pattern in order to fulfill the suggested requirement from the guidelines

- non-blocking manner
able to listen to incoming connections in a non-blocking manner
