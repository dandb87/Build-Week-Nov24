import requests
import os
import time

# Funzione per controllare i metodi HTTP abilitati
def check_all_http_methods(url):
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE']
    enabled_methods = []

    for method in methods:
        try:
            response = requests.request(method, url)
            if response.status_code != 405:  # Metodo non consentito
                enabled_methods.append(method)
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il test con metodo {method}: {e}")
    
    return enabled_methods

# Funzione per testare specifici metodi HTTP
def test_http_method(method, url):
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            payload = {"key": "value"}
            response = requests.post(url, data=payload)
        elif method == 'PUT':
            file_name = "temp_file.txt"
            open(file_name, "w").close()
            with open(file_name, "rb") as file:
                response = requests.put(url, data=file)
            os.remove(file_name)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            print(f"Errore: Il metodo {method} non è supportato per il test.")
            return False  # Segnala errore per metodi non implementati

        # Verifica lo status della risposta per i metodi gestiti
        if response.status_code in [200, 201, 204]:
            print(f"[{method}] - Status Code: {response.status_code} => Successo!")
            return True
        else:
            print(f"[{method}] - Status Code: {response.status_code} => Errore!")
            return False
    except Exception as e:
        print(f"Errore durante il test del metodo {method}: {e}")
        return False

# Funzione per selezionare i metodi con menu interattivo
def seleziona_metodi_interattivi(enabled_methods):
    #print("\nDigita i numeri corrispondenti separati da una virgola, oppure premi Invio per selezionarli tutti.")
    
    selezione = input("\nDigita i numeri corrispondenti separati da una virgola, oppure premi Invio per selezionarli tutti: ").strip()
    
    if not selezione:  # Se l'utente preme Invio senza inserire nulla
        return enabled_methods
    else:
        try:
            # Converte la selezione in una lista di numeri e filtra i metodi selezionati
            numeri_selezionati = [int(num.strip()) for num in selezione.split(",")]
            metodi_selezionati = [enabled_methods[num - 1] for num in numeri_selezionati if 1 <= num <= len(enabled_methods)]
            return metodi_selezionati
        except (ValueError, IndexError):
            print("\nSelezione non valida. Riprova.\n")
            return seleziona_metodi_interattivi(enabled_methods)

# URL del server Metasploitable2
url = "http://192.168.50.101/phpMyAdmin"

# Titolo del programma
print("\n\n********* RICERCA & VERIFICA METODI HTTP ABILITATI *********\n")
time.sleep(1.5)

# Step 1: Controllo di tutti i metodi HTTP abilitati
print("Inizio controllo di tutti i metodi HTTP abilitati...\n")
time.sleep(1.5)
all_enabled_methods = check_all_http_methods(url)

if all_enabled_methods:
    print(f"Metodi HTTP abilitati trovati su {url}:\n")
    for i, method in enumerate(all_enabled_methods, start=1):
        print(f" {i}. {method}")
else:
    print(f"Nessun metodo HTTP abilitato trovato su {url}.")
    exit(0)
time.sleep(1.5)

# Step 2: Selezione interattiva dei metodi da testare
methods_to_test = seleziona_metodi_interattivi(all_enabled_methods)

if not methods_to_test:
    print("Nessun metodo selezionato per il test. Programma terminato.")
    exit(0)

print("\nProseguo con il test delle richieste HTTP sui metodi selezionati...\n")
time.sleep(1.5)

# Step 3: Test dei metodi selezionati
has_errors = False
for method in methods_to_test:
    if not test_http_method(method, url):
        has_errors = True
    time.sleep(1.5)

# Messaggio finale
print("\n________________________________________________________________________________________")
if has_errors:
    print("\nRISULTATO: Test completato con errori. Alcune richieste non sono andate a buon fine.\n")
else:
    print("\nRISULTATO: Tutti i test sono stati completati con successo! Nessun errore rilevato.\n")
