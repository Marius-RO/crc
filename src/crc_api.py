
import struct
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    '''
    Scrieti aici numele voastre
    '''
    return "CRC API de la echipa MC-NETWORK"

def calculeaza_CRC(mesaj, polinom):

    # Scoate 0-urile din stanga
    # polinom = polinom.lstrip('0')
    len_mesaj_original = len(mesaj)
    # Facem loc restului, facand padding la dreapta cu (len(polinom) - 1) * '0'
    # deoarece restul maxim care poate ramane in urma impartirii la polinom
    # este (len(polinom) - 1) * '1'
    padding = '0' * (len(polinom) - 1)

    # Concatenam mesajul cu padding-ul de mai sus
    mesaj_cu_padding = list(mesaj + padding)

    # Cat timp mai avem cifre de '1' in mesaj_cu_padding
    while '1' in mesaj_cu_padding[:len_mesaj_original]:
        # Gaseste indexul primului '1' din mesaj_cu_padding
        index = mesaj_cu_padding.index('1')

        # Se face impartirea la polinom
        for i in range(len(polinom)):
            # Operatia de XOR.
            # Daca termenii sunt diferiti atunci se intoarce 1
            # altfel 0
            mesaj_cu_padding[index + i] = str(int(polinom[i] != mesaj_cu_padding[index + i]))

    # restul impartirii
    reminder = ''.join(mesaj_cu_padding[len_mesaj_original:])
    # pack la long
    print("reminder: ", reminder, " int: ", int(reminder, 2))
    return struct.pack("!L", int(reminder, 2))

@app.route('/crc', methods=['POST'])
def post_method():
    '''
    TODO: implementati aici un endpoint care calculeaza CRC
    '''
    # Ne bazam pe faptul ca datele vin encoded
    polinom = bin(int.from_bytes(request.data[:4], 'big'))[2:]
    # polinom = struct.unpack('!L', request.data[:4])
    mesaj = bin(int.from_bytes(request.data[4:], 'big'))[2:]
    print("polinom= ", polinom, " mesaj= ", mesaj)
    CRC = calculeaza_CRC(mesaj, polinom)
    #print(request.data)
    # return request.data
    return CRC


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
