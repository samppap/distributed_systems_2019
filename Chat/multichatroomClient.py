#Multi Chat Room
#Distributed systems 2019
#Samuel Pitkanen

###############################################################################
#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import socket, select, sys



# select the type of address and data
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

# User input for IP and Port
ip = input("IP-address: ");
port = int(input("Port: "));

# Connect to server which have been created
server.connect((ip, port));

client = input("Enter username: ");
print("");
print("Waiting for the first message...\n");

server.send(client.encode());

serverName = server.recv(1024);
serverName = serverName.decode();
# print(serverName + "has joined.");

while True:
    message = server.recv(1024);
    message = message.decode();



    print(serverName + ": " + message);
    print("");

    messageInput = input("Enter message (To quit enter STOP): ");
    messageInput = messageInput.encode();
    server.send(messageInput);


    if (messageInput == "STOP"):
        server.close();
        break;
    print("Sent! Waiting for an answer...\n");
