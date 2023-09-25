#***********************************************************************************************************************************************************************************

# Importazioni dele classi neccessarie (Notare che hx711_3 è un programma caricato dentro la schheda esp.
# Per poter richiamare questo oggetto,
# assicurarsi che i programma sia correccatemnte charicato sulla scheda) 

#import network
import urequests
from time import sleep
import time
from hx711_3 import HX711
from machine import freq
import ujson



#***********************************************************************************************************************************************************************************

# Configurazione delle informazioni di connessione a InfluxDB (Viene stabilito l'indirizzo a cui i dati verranno mandati.

# 1)   influxdb_url contiene l'indirizzo ip del database Influxdb che è satto imposatto sullla macchina virtuale (192.268.0.121),
# 2)   I numero di porta alla quale accedere (lato host) per la recezione dei dati (8086),
# 3)   Il tipo di versione del database Influxdb installata (v2),
# 4)   Il nome dell'orgnizzazione che gestisce il database Influxdb (Danieli, nottare questo nome viene sceldo dopo l'installazione del database e corrisponde al nome utente),
# 5)   Il bucket nella quale andare a scrivere i dati che verranno mandati (Estensimetro),
# 6)   E la precisione con la quale viene misurata a varialbile data (essa può essere imposatta come ms, ns, s. Nell nostro caso ms))

# Viene anche imposatto un token di accesso (essendo che per poter accedere ad un determinato bucket serve una chiave di accesso o autorizzazione),
# notare che questo tokeen da accesso a tutti i bucket anche quelli creati successivamente al token stesso 

#influxdb_url = "http://192.168.0.121:8086/api/v2/write?org=Danieli&bucket=Estensimetro&precision=ms"
#token = "ltPXXbKdwXoei8ERdTDAiFEDLqIoy5aP4PiJKO5P0yRpPhNVx0MpPFUKcwpVPF4XE1bc2AOKDzAD9aTihN_n3g=="



#***********************************************************************************************************************************************************************************

# In questo punto vengono imposatte le credenziali per l'accesso alla rete
# (Consultare il pprogramma boot.py caricato sulla scheda esp per maggiori informazioni)

'''
ssid = "TP-Link_B462"  # TPLINK
password "

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print("Connessione in corso alla rete WiFi...")
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        pass
print("Connessione WiFi stabilita")
print("Indirizzo IP:", sta_if.ifconfig()[0])
'''



#***********************************************************************************************************************************************************************************

# Viene definita una funzione per l'acquisizione della data corrente locale in millisecondi

# 1)   Nel dettaglio ci si appogggia alla funzione time_ns che da come output la data UTC a partire dal 1° gennaio 2000, 00:00:00 con precisione in nanosecondi
#      (questa scelta di precisione è stata decisa in quanto il modulo di acquiosizione hx711 è molto veloce nella lettura,
#      per tanto i millisecondi non erano abbastanza per differenziare il dato rischiando una sovrascrittura di alcuni valori)

# 2)   Il tempo acquisito in current_time_nseconds viene convertito in millisecodni dopo essere certi che la lettura della data è stata differenziata dalle altre

# 3)   Viene aggiunto l'offset di 946684800000 per arrivare alla data corrente

# 4)   Sottraggo alla variabile current_time_milliseconds il tempo in eccesso sulla data che in questo caso corrispponde a due ore esatte 

'''
def get_utc_time_with_milliseconds():
    
    # Punto 1
    current_time_nseconds = time.time_ns()
    
    # Punto 2, Conversione da nanosecondi in milisecondi
    current_time_milliseconds = current_time_nseconds // 1000000
    
    # Punto 3, Aggiungo offset
    current_time_milliseconds += 946684800000  
    
    # Punto 4, Sottraggo due ore
    current_time_milliseconds -= 2 * 60 * 60 * 1000
    
    return current_time_milliseconds
'''


#***********************************************************************************************************************************************************************************

# Funzione per formattare i dati in una stringa compatibile con InfluxDB

# Per poter comunicare con il database serve una formattazione speecifica della stringa iin maniera che l'host siia in grado di leggere

# La stringa è {measurement},{tag}={tag_value} {field}={field_value} {time} (Notare che spazi e virgole non sono casuali ma vanno rispettai)
# 1)   mesurement indica il nome della misurazione (nel nostro caso viene passato come argomento della funzione e corrisponde a Distosione)
# 2)   tag, esso viene identificata come tag=tag_value dove il primo valore indica il nome del tag il secondo il valore che può essere stringa o intero
#      (Nota che se si vuole inserire più di un tag basta aggiungere una virgola e un altro tag con la stessa sintassi senza inserire spazi es. tag1=tag_value1,tag2=tag_value2)
# 3)   field, esso viene identificata come field=field_value dove il primo valore indica il nome del field il secondo il valore che può essere stringa o intero
#      (Nota che se si vuole inserire più di un field basta aggiungere una virgola e un altro field con la stessa sintassi senza inserire spazi es. field1=field_value1,field2=field_value2)
# 4)   time, esso serve ad identificare l'orario in cui avviene la lettura della misurazione, esso è un valore aggiuntivo ma è consigliato l'inserimento per eviitare sovrascritture di dati

'''
def format_influxdb_data(measurement, tag, tag_value, field_1, field_value_1, field_2, field_value_2, timestamp):
    data_string = "{measurement},{tag}={tag_value} {field_1}={field_value_1},{field_2}={field_value_2} {time}".format(
        measurement=measurement,
        tag = tag,
        tag_value = tag_value,
        field_1 = field_1,
        field_value_1 = field_value_1,
        field_2 = field_2,
        field_value_2 = field_value_2,
        time = timestamp
    )
    return data_string

'''

def load_data():
    try:
        with open('settaggio.json', 'r') as file:
            data = ujson.load(file)
            return data.get('value', {})
    except OSError:
        print("Errore durante la lettura del file")
        return {}

'''
def save_data(value_data):
    try:
        with open('settaggio.json', 'r') as file:
            data = ujson.load(file)
        data['value'] = value_data
        with open('settaggio.json', 'w') as file:
            ujson.dump(data, file)
    except OSError:
        print("Errore durante la scrittura del file")

'''
def save_data(value_data):
    try:
        dictionary = {
            "name": "sathiyajith",
            "rollno": 56,
            "cgpa": 8.6,
            "phonenumber": "9976770500"
        }
         
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
         
        # Writing to sample.json
        with open("prova.json", "w") as outfile:
            outfile.write(json_object)
            
    except OSError:
        print("Errore durante la scrittura del file")
#***********************************************************************************************************************************************************************************

# Configurazioen modulo di amplificazione HX711

# 1)   In questo punto viene deciso su quali pin fisici della cheda esp32 il modulo HX711 dovrà eseguire la lettura
# (Nota che la variabile d_out corrisponde a DO/RX sul modulo fisico HX711 alla quale è associato il pin D16 della scheda esp32,
# mentre la variabile pd_sck corrisponde a CK/... sul modulo fisico HX711 alla quale è associato il pin D4 della scheda esp32)
# 2)   Viene scelto il canale e la velocità di lettura (Nota al momento il modulo HX711 è dalsato all'estensimetro per tanto l'unico canale utilizzabile è l'A)
# 3)   Viene esegiuto un ciclo di misurazioni senza scrittura del dato dalla durata di 2 secondi (questo processo è essenziale per la stabilizzazione del dato al primo avvio
#      in quanto impiega qualche secondo a raggiungere il punto di stabiilità l'estensimetro) 

freq(160000000)

print("prova1")

# Punto 1
driver = HX711(d_out=16, pd_sck=4)
driver2 = HX711(d_out=22, pd_sck=23)

'''
print("prova2")

sleep(2)

driver2 = HX711(d_out=17, pd_sck=5)

print("prova3")

'''

# Punto 2
#driver.channel=HX711.CHANNEL_A_64
driver.channel=HX711.CHANNEL_A_128
#driver.channel=HX711.CHANNEL_B_32

i = 0
r_old = 0
r_old2 = 0

# Punto 3
#timeout = time.time() + 2    2 seconds
while True:

    #**************************************************************************************************************************************
    # Driver 1
    gain = 130/136000
    va=4.1
    g=2.5
    zero=170
    offset = 87080
    alfa = 0.1

    r = driver.read()
    r_fil = (r*alfa) + (r_old * (1-alfa))
    r_old = r_fil
    vs=r/gain
    epsilon= 2*(vs-zero)/(va*g)
    peso = (r_fil - offset)*gain
    
    print("nm/m 1: ")
    print(epsilon)
    #print(r_fil)
    #print(peso)
    
    #y = 0
    sleep(1)
    
    
    #**************************************************************************************************************************************
    # Driver 2
    
    gain = 130/136000
    va=4.1
    g=2.5
    zero=170
    offset = 87080
    alfa = 0.1

    r = driver2.read()
    r_fil = (r*alfa) + (r_old2 * (1-alfa))
    r_old = r_fil
    vs=r/gain
    epsilon= 2*(vs-zero)/(va*g)
    peso = (r_fil - offset)*gain
    
    print("nm/m 2: ")
    print(epsilon)
    
    
    #print(r_fil)
    #print(peso)
    
    #y = 0
    sleep(1)



#***********************************************************************************************************************************************************************************

# In questa parte di codice è divisa in due cicli annidati 
# 1)   Il primo ciclo indica quante volte il buffer verra riempito (Nota, normalmente per avere una versione continuativa del programma andrebbe imposatto come while true,
#      per questa versione di prova ho deciso di mettere una fine al ciclo)
# 2)   Il secondo ciclo indica la quantità dei valori che verranno inseriti nel buffer (Nota, la scheda esp32 ha una capacita limitata di meorizzazione dei dati,
#      ho riscontrato che quando supera i 440 vaori circa va in errrore a causa dello spazio insufficente,
#      al momento è stato imposatto a 90 valori in quanto il programma manda due dati differenti e non uno solo, questo valore può variare)
# 3)   Settaggio delle variabili che servono per la trasmissione dei dati l database Influxdb

# Punto 1
while y < 3:
    
    # Dati da inviare a InfluxDB
    #********************************************************************************************************
    i = 0
    data = ""
    
    # Punto 2
    while i < 90:
                
        #('A', 64)
        #gain=524
        gain = 130/136000
        va=4.1
        g=2.5
        zero=170
        offset = 87080
        alfa = 0.1

        r = driver.read()
        r_fil = (r*alfa) + (r_old * (1-alfa))
        r_old = r_fil
        vs=r/gain
        epsilon= 2*(vs-zero)/(va*g)
        peso = (r_fil - offset)*gain
        #print(epsilon)
        print(r_fil)
        print(peso)

        
        # Punto 3
        measurement = "Distorsione"
        tag_name = "sensor"
        tag_value = "Estensimetro"
        field_name_1 = "valueEstensimetro"
        field_value_1 = peso
        field_name_2 = "indice"
        field_value_2 = int(i)
        current_utc_time_with_milliseconds = get_utc_time_with_milliseconds()

        data += format_influxdb_data(measurement, tag_name, tag_value, field_name_1, field_value_1, field_name_2, field_value_2, current_utc_time_with_milliseconds)
        data += '\n'

        print(i)
        
        i += 1
        
        #sleep(1)

    # Invio della richiesta HTTP a InfluxDB
    headers = {"Authorization": "Token {}".format(token)}
    response = urequests.post(influxdb_url, data=data, headers=headers)

    # Verifica della risposta del server InfluxDB
    if response.status_code == 204:
        print("Dati inviati con successo a InfluxDB")
        print(i)
    else:
        print("Errore durante l'invio dei dati a InfluxDB:", response.text)

    # Chiusura della connessione
    response.close()
    
    y += 1
    
driver.power_off()





    



