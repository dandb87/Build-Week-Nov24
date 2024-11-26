import requests
import os
import time

# Flag per monitorare errori
has_error = False

# URL per ogni tipo di richiesta
base_url_get = "http://192.168.50.101/twiki/bin/view/Main/WebHome"
base_url_post = "http://192.168.50.101/twiki/bin/save/Main/WebHome"
base_url_put = "http://192.168.50.101/dav/"
base_url_delete = "http://192.168.50.101/dav/"

print("\n\n ************** TEST HTTP **************")
time.sleep(1)
print("\nInizio test...")
time.sleep(1)


# Richiesta GET
response_get = requests.get(base_url_get)
if response_get.status_code == 200:  # Gestione errori
    print(f"\n[Richiesta GET] - Status Code: {response_get.status_code} => Tutto ok!")
else:
    print(f"\n[Richiesta GET] - Status Code: {response_get.status_code} => Errore!")
    has_error = True
time.sleep(1)


# Richiesta POST
payload_post = {"text": "Nuovo contenuto", "topic": "Main.WebHome", "save": "Save"}
response_post = requests.post(base_url_post, data=payload_post)
if response_post.status_code == 200:  # Gestione errori
    print(f"\n[Richiesta POST] - Status Code: {response_post.status_code} => Tutto ok!")
else:
    print(f"\n[Richiesta POST] - Status Code: {response_post.status_code} => Errore!")
    has_error = True
time.sleep(1)


# Richiesta PUT
file_name = "mio_file.txt"  # Creazione del file temporaneo vuoto
open(file_name, "w").close()  # Crea un file vuoto
url_put = "http://192.168.50.101/dav/mio_file.txt"  # URL del file
with open(file_name, "rb") as temp_file:
    response_put = requests.put(url_put, data=temp_file)
if response_put.status_code in [200, 201, 204]:  # Gestione errori
    print(f"\n[Richiesta PUT] - Status Code: {response_put.status_code} => Tutto ok!")
else:
    print(f"\n[Richiesta PUT] - Status Code: {response_put.status_code} => Errore!")
    has_error = True
if not os.path.exists(file_name):
    print(f"\nErrore: {file_name} non trovato!")
time.sleep(1)


# Richiesta DELETE
url_delete = "http://192.168.50.101/dav/mio_file.txt"  # URL del file da eliminare
response_delete = requests.delete(url_delete)
if response_delete.status_code in [200, 204]:  # 204 è valido per DELETE
    print(f"\n[Richiesta DELETE] - Status Code: {response_delete.status_code} => Tutto ok!")
    # Elimina il file locale
    if os.path.exists(file_name):
        os.remove(file_name)
        #print(f"\nIl file '{file_name}' è stato eliminato correttamente.")
    else:
        print(f"\nIl file '{file_name}' non esiste più o non è stato trovato.")
else:
    print(f"\n[Richiesta DELETE] - Status Code: {response_delete.status_code} => Errore!")
    has_error = True
time.sleep(1)


# Messaggio finale
print("_________________________________________________________________")
if has_error:
    print("\nRISULTATO: Attenzione! Una o più richieste hanno generato errori\n\n")
else:
    print("\nRISULTATO: Tutte le richieste sono state completate con successo!\n\n")
