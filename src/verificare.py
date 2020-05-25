import requests
import struct


url = 'http://ec2-35-173-126-158.compute-1.amazonaws.com:8001/crc'
header = {'Content-Type': 'application/octet-stream'}

# trimitem polinomul 44 si mesajul mesaj catre url pentru a-i fi calculat crc ul 
polinom = struct.pack('!L', 44)
mesajul = 'mesaj'.encode('utf-8')

de_trimis = polinom + mesajul

# in urma cererii post va fi returnata valoarea crc - ului 
response = requests.post(url, headers=header, data=de_trimis)

print("CRC primit: ", struct.unpack("!L", response.content)[0])
