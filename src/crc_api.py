
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

    # lungimea mesajul original (fara padding) ne va ajuta la impartire
    # (stim pana unde sa facem impartirea)
    len_mesaj_original = len(mesaj)

    # Facem loc restului, facand padding la dreapta cu (len(polinom) - 1) * '0'
    # deoarece restul maxim care poate ramane in urma impartirii la polinom este (len(polinom) - 1) * '1'
    # 
    # Ex: pentru un polinom de 4 biti sa spune 1101 si meajul 1011011 vom adauga 4 - 1 biti la finalul mesajului
    # astfel ca mesajul cu padding va fi 1011011000
    #
    # La final (dupa impartire) acesti biti de padding vor reprezenta valoarea restului impartirii, iar in cazul de fata unde
    # polinomul este pe 4 biti , valoarea acestuia va fi intre 000 si 111 inclusiv.
    padding = '0' * (len(polinom) - 1)

    # Mesajul prelucrat mai departe va fi cel cu padding ul adaugat, astfel ca vom concatena mesajul original cu padding ul
    mesaj_cu_padding = list(mesaj + padding)

    # Cat timp mai avem cifre de '1' in mesaj_cu_padding (adica cat timp mai putem face impartirea)
    while '1' in mesaj_cu_padding[:len_mesaj_original]:

        # Gaseste indexul primului '1' din mesaj_cu_padding
        # adica indexul primului '1' din dreapta
        index = mesaj_cu_padding.index('1')

        # Se face impartirea mesajului cu padding la polinom

        # pentru fiecare bit din polinom si fiecare bit corespunzator din mesajul de padding
        # (daca le-am aseza deasupra ar fi bitul de deasupra sa)
        for i in range(len(polinom)):
            # se aplica operatia de XOR (daca termenii sunt diferiti atunci se intoarce 1, altfel 0)
            # valoarea Booleana != se va transforma in 0 daca este False si 1 daca este True
            # mesaj_cu_padding[index + i] este bitul corespunzator din mesajul cu padding (cel de deasupra bitului din polinom)
            mesaj_cu_padding[index + i] = str(int(polinom[i] != mesaj_cu_padding[index + i]))

            
    # restul impartirii optinut in urma impartirii repetate a mesajului ramas la polinom
    reminder = ''.join(mesaj_cu_padding[len_mesaj_original:])
    # print("reminder: ", reminder, " int: ", int(reminder, 2))

    # in acest moment restul este un string normal de caractere, unde caracterele sunt 0 sau 1
    # se face conversia acestui sir intr-o valoare intreaga folosind functia int(reminder, 2), unde 2 reprezinta baza de conversie
    # si se face pack la respectiva valoare pe un long
    return struct.pack("!L", int(reminder, 2))


@app.route('/crc', methods=['POST'])
def post_method():
    # datele vor veni ca un string de biti stfel ca vom face conversie intr-un string binar (numai cu 1 si 0)
    # care va fi trimis mai departe spre calulul crc - ului

    # se face extragerea int.from_bytes(..., 'big') pentru ca sirula care se primeste trebuie convertit intr-un sir binar de 
    # 0 si 1, atat pentru valoarea polinomului cat si pentru mesaj
    # big reprezinta modul de conversie, adica big endian
    

    # polinomul este reprezentat de request.data[:4]  
    polinom = bin(int.from_bytes(request.data[:4], 'big'))[2:] # folosim [2:] pentru a elimina 0b de la inceputul stringului binar

    # mesajul este reprezentat de request.data[4:] 
    mesaj = bin(int.from_bytes(request.data[4:], 'big'))[2:] # folosim [2:] pentru a elimina 0b de la inceputul stringului binar

    # print("polinom= ", polinom, " mesaj= ", mesaj)

    return calculeaza_CRC(mesaj, polinom)
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
