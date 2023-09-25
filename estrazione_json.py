#import ujson
import json
import os

values = {}

def load_data():
    try:
        with open('settaggio.json') as file:
            print("A")
            data = ujson.load(file)
            print("A")
    except OSError:
        print("Errore durante la lettura del file")
        return None

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


def read_directory(directory):
    try:
        files = os.listdir(directory)
        return files
    except OSError:
        print(f"Errore durante la lettura della directory {directory}")
        return None
    
def extract_values(data):
    connessione = data.get("Connessione", {})
    influx_dati = data.get("Influx_dati", {})
    influx_connessione = data.get("Influx_connessione", {})
    estensimetri = data.get("Estensimetri", [])
    dati_partenza = data.get("Dati_partenza", {})

    return connessione, influx_dati, influx_connessione, estensimetri, dati_partenza

'''
# Esempio di utilizzo:
# Leggi dati dal file JSON
#values = load_data()
if values is not None:
    #print("Dati letti:", values)

    # Modifica i dati
    #values['Connessione']['SSID'] = 'NuovoSSID'
    #values['Dati_partenza']['Gain'] = 'NuovoGain'

    # Salva i dati nel file JSON
    #save_data(values)
    
    connessione, influx_dati, influx_connessione, estensimetri, dati_partenza = extract_values(values)
    
    SSID = connessione.get("SSID",None)
    
    print (SSID)
    
    connessione["SSID"] = "sustrato2"
    
    print(values)
    print(connessione.get("SSID",None))
    
    save_data(values)

    # Stampa le liste
    print("Connessione:", connessione)
    print("Influx_dati:", influx_dati)
    print("Influx_connessione:", influx_connessione)
    print("Estensimetri:", estensimetri)
    print("Dati_partenza:", dati_partenza)
    
    '''

try:
    '''
    dictionary = {
        "name": "sathiyajith",
        "rollno": 56,
        "cgpa": 8.6,
        "phonenumber": "9976770500"
    }
     
    # Serializing json
    json_object = json.dumps(dictionary)
     
    # Writing to sample.json
    with open("prova.json", "w") as outfile:
        outfile.write(json_object)
        
    json_object.close()
    '''
    
    value2 = {}
    value ={  
              "Connessione": {
                "SSID": "TP-Link_B462",
                "Password": "91417558",
                "Indirizzo_IP": "197.103.0.110"
              },
              "Influx_dati": {
                "Measurement": "Estensimetro",
                "Tag_1": "Lato",
                "Tag_2": "Numero_astuccio",
                "Field": "Strain_nm"
              },
              "Influx_connessione": {
                "Bucket": "Estensimetro",
                "Org": "Danieli",
                "Token": "12345"
              },
              "Estensimetri": [
                {
                  "Estensimetro_1": {
                    "d_out": 16,
                    "pd_sck": 4
                  }
                },
                {
                  "Estensimetro_2": {
                    "d_out": 22,
                    "pd_sck": 23
                  }
                }
              ],
              "Dati_partenza": {
                "Gain": "130/13600",
                "Gauge_factor": 2.5444,
                "Va": 4.1,
                "Zero": 170
              }

    }
    
    
    json_string = json.dumps(value)

    # Apri il file in modalità scrittura
    with open("savedata.json", "w") as save_file:
    # Scrivi la stringa JSON nel file
        save_file.write(json_string)
        
except OSError:
    print("Errore durante la scrittura del file")
    
    
try:
    with open('savedata.json', 'r') as file:
        data = json.load(file)
        data.get('value2', {})
except OSError:
    print("Errore durante la lettura del file")
    

print(value2)
