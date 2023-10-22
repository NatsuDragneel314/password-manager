from cryptography.fernet import Fernet
import tkinter as Tk
from tkinter.messagebox import showerror,showinfo,showwarning
import json,os,getpass,pyperclip,smtplib,ssl
from random import randint,random

def generate_key():
    return Fernet.generate_key()

def initialize_cipher(key):
    return Fernet(key)

import secrets
import string

# define the alphabet
letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation

alphabet = letters + digits + special_chars

# fix password length
pwd_length = 6
# generate password meeting constraints
while True:
  pwd = ''
  for i in range(pwd_length):
    pwd += ''.join(secrets.choice(alphabet))

  if (any(char in special_chars for char in pwd) and 
      sum(char in digits for char in pwd)>=2):
          break


def encrypt_passowrd(cipher,password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(cipher,encrypt_password):
    return cipher.decrypt(encrypt_password.encode()).decode()

def view_websites():
    try:
        with open('passwords.json','r') as data:
            view=json.load(data)
            print("\nwebsites you saved...\n")
            for x in view:
                print(x['website'])
            print('\n')
    except FileNotFoundError:
        print("You have not saved any passords!!")

key_filename="key.key"
if os.path.exists(key_filename):
    with open(key_filename,'rb') as key_file:
        key=key_file.read()
else:
    key=generate_key()
    with open(key_filename,'wb') as key_file:
        key_file.write(key)

cipher=initialize_cipher(key)

def add_password(website,password):
    if not os.path.exists('password.json'):
        data=[]
    else:
        try:
            with open('passwords,json','r') as file:
                data=json.load(file)
        except json.JSONDecodeError:
            data=[]
    
    encrypted_passowrd=encrypt_passowrd(cipher,password)

    password_entry={'website':website,
                    'password':encrypted_passowrd}
    data.append(password_entry)


    with open("passwords.json",'w') as file:
        json.dump(data,file,indent=4)

def get_password(website):
    if not os.path.exists("passwords.json"):
        return None
    try:
        with open("passwords.json",'r') as file:
            data=json.load(file)
    except json.JSONDecodeError:
        data=[]

    for entry in data:
        if entry['website']==website:
            decrypted_password=decrypt_password(cipher,entry['password'])
            return decrypted_password
    return None    

import smtplib
from email.mime.text import MIMEText
subject = "Email Subject"
body = f"This is the body of the text message {pwd}"
sender = "arthurlewin2255@gmail.com"
recipients = "jackdenin17@gmail.com"
password = "xmwr ofpt cyer sgtm"


def send_email(subject, body, sender, recipients, password):
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
                print("Message sent!")

while True:
    print("1.login")
    print('2. quit')
    choice=input("enter your choice: ")
    if choice == "1":
        send_email(subject, body, sender, recipients, password)
                
        masterpassword=input("Enter opt: ")

        if masterpassword==pwd:
            while True:
                print("1. Add Password")
                print("2. Get Password")
                print("3. view saved websites")
                print("4. quit")
                password_choice= input("Enter your choice:")
                if password_choice == "1":
                    website =input("enter website:")
                    password = getpass.getpass("Enter password:")
                    add_password(website,password)
                    print('\n Password added!!')

                elif password_choice == '2':
                    website = input("Enter website: ")
                    decrypted_password = get_password(website)
                    if website and decrypted_password:
                    # Copy password to clipboard for convenience
                        pyperclip.copy(decrypted_password)
                        print(f"\n[+] Password for {website}: {decrypted_password}\n[+] Password copied to clipboard.\n")
                    else:
                        print("\n[-] Password not found! Did you save the password?"
                                "\n[-] Use option 3 to see the websites you saved.\n")
                    
                elif password_choice == '3':  # If a user wants to view saved websites
                    view_websites()
                elif password_choice == '4':  # If a user wants to quit the password manager
                     break
                
        else:
            print("wrong password!!")

    elif choice == '2':  # If a user wants to quit the program
       break


#xmwr ofpt cyer sgtm