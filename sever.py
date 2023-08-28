'''
import the libraries

create function for broadcast , main and client connections handling

1) Broadcast function (broadcast(message))  = the message taken from function and broadcasted 
   to every client currently present in the machine

   Required functions:
   client.send(<message encoded in utf-8 format />)

2) Handle client connection (handleClientConnections(<client socket> , <username>)) = the 
   function handle client mangment such as adding the client ,removing the client and error 
   handling

   Required function :
   for recieving message = CSoc.recv(1024).decode("utf-8")
   for sending message to that client use CSoc.send(<message >)
   for closing client = CSoc.close()
   Remove client from dictionary = del <dictionary name>[<id of desired pair>]
   for broadcasting to everyone we use broadcast function = broadcast(<message >)
   for chatting we use brodcast message and user name to highlight who sent which mesage

   Note :
   As users keep getting added we need to use while loop continuously 
   As some error might happen so try catch black is added for error handling

3) Server initiation function(main()) = in this function we define port and host , initilise 
   socket io and store in server variable , then we bind the socket with port and address .
   after binding we start server and listen for upcoming requests 


Questions :
1) what are web sockets and why do we need them?
Ans : i) WebSockets are a communication protocol that provides full-duplex, bidirectional communication
      channels over a single TCP connection
      ii) suitable for applications that require real-time, interactive, and dynamic
      communication between clients and servers.

2) what is need for encoding before sending messages in websocket context and why use utf-8
Ans : i) Messae remains consistent, utf-8 works with various langugaes and sysmbols as well as compatible
         over various platforms

3) 5 pending request in queue
Ans : i) it limits concurrent connections 

'''

import socket
import threading

connected_clients = {}


def broadcast(message):
    for client in connected_clients.values():
        client.send(message.encode('utf-8'))

# now we have to handle client connectionss
# mainly we dp the 3 types of actions to it , and it should be running continuespuly,so use while loop
# 1) if there is some error then handle it
# 2) if client has sent leave message in lower or upper case then kick the client out
# 3) if a message is sent then broadcast the message to everyone

# the client and username is recieved


def handleClientConnections(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            elif (message.lower() == "leave"):
                # drop the client and tell everyone
                # SEND THE DROP ack
                # drop the client
                # remove the record from dic
                # broad cast the name of client who left and then break
                client_socket.send(
                    "You have left the chat room.".encode("utf-8"))
                client_socket.close()
                del connected_clients[username]
                broadcast(f"{username} has left the chat.")
                break
            else:
                broadcast(
                    f" the username of new joinee is {username} and the message is {message}")

        except:
            break


def main():
    port = 1122
    host = "127.0.0.1"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((host, port))

    server.listen(5)
    print(f"socket is listening on port {port} and host {host}")

    while True:
        CSoc, CAdd = server.accept()
        uname = CSoc.recv(1024).decode("utf-8")
        connected_clients[uname] = CSoc
        print(f"{uname} conected from {CAdd}")
        CSoc.send("welcome to the server ".encode("utf-8"))

        broadcast(f"{uname} is jusy joined the chat")
        CThread = threading.Thread(
            target=handleClientConnections, args=(CSoc, uname))
        CThread.start()


if __name__ == "__main__":
    main()
