import os
import random
import socket
import string
import subprocess
import sys
from threading import Thread
import time

# Global vars
chars = string.ascii_letters + string.digits + string.punctuation
loggedUser = ["Benito", "c9v#M7_6"]
passlen = 8
threads = []

#################################
   
def manage_account(conn):
    msg = "Hey, {}! Welcome back\n".format(loggedUser[0])
    msg += "As you know, we are a very secure company. Therefore, you will not know your password. This way you can't be hacked!\n"
    conn.send(msg.encode())      

def checkBalance(conn, balance):
    message = "Here you can check how much money you have left in your account.\n"
    conn.send(message.encode())
    time.sleep(0.2)
    msg = loggedUser[0]+", your current balance is: "+str(balance)+"$.\n"
    conn.send(msg.encode())

def transferMoney(conn, balance):
    message = "Here you can transfer money to other bank accounts. Be careful tho, our systems are a little old.\n\n"
    conn.send(message.encode())
    message = "Enter amount:\n"
    conn.send(message.encode())
    amount = conn.recv(50).decode().strip()
    message = "Enter destination account:\n"
    conn.send(message.encode())
    account = conn.recv(1024).decode().strip()

    conn.send("Enter your password to confirm the transaction:\n".encode())
    password = conn.recv(1024).decode().strip()
    cont = 0
    if len(loggedUser[1]) != len(password):
        conn.send("Password lengths must match".encode())
        return

    for i in range(len(loggedUser[1])):
        if loggedUser[1][i] == password[i]:
            time.sleep(0.25)
            cont += 1
    
    if cont == len(loggedUser[1]):
        if int(amount) > 0 and int(amount) <= balance:
            balance -= int(amount)
            message = "Succesfully sent "+amount+"$ to account "+account+".\n"
            conn.send(message.encode())
        else:
            conn.send("The amount entered is invalid or there is not enough money in your account.\n".encode())
    else:
        conn.send("Wrong password!\n".encode())

def accessSafe(conn):
    print("\t -> Accessing safe")
    message = "Welcome to your super secure safe!\n"
    message += "It was made with the latest technology, where you will be able to store your most valuable information 🚩.\n\n"
    message += "But first, please enter your password to access your safe:\n"
    conn.send(message.encode())
    passw = conn.recv(1024).decode().strip()
    if passw == loggedUser[1]:
        message = "Access granted!\n"
        message += "Here is your flag: CTFUni{El_t13mp0_3s_0R0!$}\n"
        conn.send(message.encode())
    else:
        message = "Access denied!\n"
        conn.send(message.encode())

    print("\t -> Tried password:", passw)

def prompt_menu(conn):
    message = "Welcome to the SuperSecureBank!\n"
    message += "--------------------------------\n"
    conn.send(message.encode())

    manage_account(conn)
    balance = 100

    while True:
        message = "\n\nPlease select an option:\n"
        message += "--------------------------------\n"
        message += "1. Check your current balance\n"
        message += "2. Transfer money\n"
        message += "3. Access your super secure safe\n"
        message += "4. Exit\n"
        conn.send(message.encode())

        validOption = False

        while not validOption:
            response = conn.recv(10).decode().strip()
            print("Received option:", response)
            if response == "1" or response == "2" or response == "3":
                validOption = True
            elif response == "4":
                conn.send("Thank you for using our services!\n".encode())
                conn.close()
            else:
                conn.send("Invalid option. Please try again.\n".encode())

        if response == "1":
            checkBalance(conn, balance)
        elif response == "2":
            transferMoney(conn, balance)
        elif response == "3":   
            accessSafe(conn)


# Main program
if __name__ == "__main__":    
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 10000)
    print('> Starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        try:
            # Wait for a connection
            print('> Waiting for a connection...')
            connection, client_address = sock.accept()
            print('\t -> Connection from', client_address)
            t = Thread(target=prompt_menu, args=[connection])
            threads.append(t)
            t.start()
        except:
            print("Error")

    for t in threads:
        t.join()   

