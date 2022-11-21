##
# Authors: Ryan Burkhalter and Josh Vancleave
##
FILES_DIR = "files/"#Where the text files are intended to be placed.
MY_KEYS_DIR = "my_key_pairs/"#Location of private keys
PUBLIC_KEYS_DIR = "public_keys/"#Location of public keys
SHARED_KEYS_DIR = "shared_keys/"#Location of shard keys
RSA_EXTN = ".rsa"#RSA key file extension
import socket
import ipaddress
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
import os
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
PORT = 65432  # The port used by the server
def menu():
    option = ""
    while(option != "0"):
        print("====Secure Communicator====")
        print("----Main Menu----")
        print("1) Generate RSA key pairs")
        print("2) View RSA key pairs")
        print("Send Message")
        print("Receive Message")
        print("0) exit")
        print("Enter Option: ")
        option = input()
        if(option == "1"):
            generate_rsa()
        elif (option == "2"):
            view_keys()
        elif (option == "3"):
            send()
        elif (option == "4"):
            recieve()
        elif (option == "0"):
            print("\nGoodbye!")
            exit(1)
        else:
            print("Error, invalid input")

def send():
    messageChecked = False
    message = ""
    while(messageChecked == False):
        message = input("Enter Message (max 4096 characters): ")
        if(len(message) > 4096):
            print("Please limit message to 4096 characters.")
        else:
            messageChecked = True
    target = ""
    validIP = False
    while (validIP == False):
        target = input("Enter Recipient IP: ")
        try:
            ip_object = ipaddress.ip_address(target)
            validIP = True
        except ValueError:
            print("Error not a valid IPv4:")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(30.0)#Time out of 30 seconds if not received
        s.connect((target, PORT))
        s.settimeout(None)#Always set timeout to none before sending.
        s.sendall(bytes(message, 'utf-8'))
        data = s.recv(1024)
        if (data == b"#<<END>>#"):
            print("Message sent successfully")
    except:
        print("Message sending error. Message not sent")


def recieve():
    ALL_IP = ""
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ALL_IP, PORT)) #Inner brackets define a tuple
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            exit = False
            while not exit:
                data = conn.recv(1024)
                if not data:
                    exit = True
                else:
                    print("Message:")
                    print(data.decode(),end="\n")
                    print("End of message.")
                conn.sendall(b"#<<END>>#")

def generate_rsa():
    key_name = input("Enter name for keys> ")
    key = RSA.generate(2048)
    f = open('./my_key_pairs/' + key_name + '_prv.rsa','wb')
    f.write(key.export_key('PEM'))
    f.close()

    public_key = key.public_key()
    f = open('./my_key_pairs/' + key_name + '_pub.rsa','wb')
    f.write(public_key.export_key('PEM'))
    f.close()

def view_keys():
    files = os.listdir('./my_key_pairs')
    print("======Own Key Pairs======")
    for i in files:
        print(i)
menu()