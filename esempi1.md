# Tasks

## ESP32
- 1 esp32 su ogni astuccio, 4 ingressi ogni esp32
- hmi page:
  - valori istantanei
  - impostazioni variabili
- attivare webrepl

### dati setup e salvataggio:
|Nome|Configurazione|Setup|Note|
|----------|----------|---------|----------|
|Rete, pw, indirizzo IP|x|
|polling|x|
|records|x|
|Ingresso.A.1.pin|x|
|Ingresso.A.1.gain|x|x|
|Ingresso.A.1.offset|x|x|
|Ingresso.A.1.tags|x|
|Ingresso.A.1._field|x|
|Ingresso.A.1.value|||ultimo valore letto|
|Influxdb.addr|x|
|Influxdb.token|x|
|Influxdb._measurement|x|

## Influxdb
Dato:  
estensimetri,astuccio=1,lato=1 streinght=11  
estensimetri,astuccio=1,lato=2 streinght=12  
estensimetri,astuccio=1,lato=3 streinght=13  
estensimetri,astuccio=1,lato=4 streinght=14  

## Docker
- influxdb
- ntp
- python plc read
