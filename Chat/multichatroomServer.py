#Multi Chat Room
#Distributed systems 2019
#Samuel Pitkanen

###############################################################################
#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import socket, select, sys

def HandleServer():
        # select the type of address and data
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        # User input
        ip = str(input("IP-address: "));
        port = int(input("Port: "));

        # binds the selected IP and port together
        server.bind((ip, port));
        server.listen(15);

        client = input("Enter username: ");
        print("");
        print("Waiting for connections...");

        
        connection, address = server.accept();
        serverName = connection.recv(1024);
        serverName = serverName.decode();


        print(serverName + " has joined!\n");

        connection.send(client.encode());



        return connection, address, serverName;



def HandleMessage (connection, address, serverName):


    message = input("Enter message (To quit enter STOP): ");
    if (message == "STOP"):
        connection.close();
        return 0;
    else:
        connection.send(message.encode());
        print("Sent! Waiting for an answer...\n");

        message = connection.recv(1024);
        message = message.decode();

        print(serverName +  ": " + message);
        print("");



connection, address, serverName = HandleServer();

while True:
    if (HandleMessage(connection, address, serverName) == 0):
        break;
