import socket
import time

def is_host_reachable(target_ip):
    """Verifica se l'host è raggiungibile tramite una connessione di test."""
    try:
        # Prova una connessione rapida alla porta 80 (HTTP)
        with socket.create_connection((target_ip, 80), timeout=3):
            return True
    except (socket.timeout, socket.error):
        return False

def scan_ports(target_ip, start_port, end_port):
    open_ports = []  # Lista per porte aperte
    filtered_ports = []  # Lista per porte filtrate
    closed_count = 0  # Contatore per porte chiuse

    print(f"\nScansione in corso su {target_ip} da porta {start_port} a porta {end_port}...\n")
    time.sleep(1)

    for port in range(start_port, end_port + 1):
        try:
            # Crea un socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Timeout di 1 secondo
                # Prova a connettersi alla porta
                result = s.connect_ex((target_ip, port))
                if result == 0:  # Porta aperta
                    try:
                        protocol = socket.getservbyport(port).upper()
                    except OSError:
                        protocol = "SCONOSCIUTO"
                    open_ports.append(f"Porta {port}: Aperta (Protocollo: {protocol})")
                elif result == 10060:  # Timeout -> Porta filtrata
                    filtered_ports.append(f"Porta {port}: Filtrata")
                else:  # Porta chiusa
                    closed_count += 1  # Incrementa il contatore
        except Exception as e:
            print(f"Errore durante la scansione della porta {port}: {e}")
        time.sleep(0.05)  # Ritardo tra ogni scansione

    # Stampa i risultati
    print("\n*********** RISULTATI SCANSIONE ***********\n")
    
    print(f"PORTE APERTE ({len(open_ports)}):")
    if open_ports:
        print("\n".join(open_ports))
    else:
        print("Nessuna porta aperta trovata.")
    
    print(f"\nPORTE FILTRATE ({len(filtered_ports)}):")
    if filtered_ports:
        print("\n".join(filtered_ports))
    else:
        print("Nessuna porta filtrata trovata.")
    
    # Messaggio per le porte chiuse
    print(f"\nPORTE CHIUSE:({closed_count})")
    print(f"Le restanti {closed_count} porte sono chiuse.")


# Chiedi all'utente l'indirizzo IP e il range di porte da scansionare
print("\n *************** PORT SCANNER ***************")
target_ip = input("\nInserisci l'indirizzo IP da scansionare: ")

if not is_host_reachable(target_ip):
    print(f"\nErrore: l'host {target_ip} non è raggiungibile. Controlla la connessione o il firewall.")
    exit()

try:
    start_port = int(input("\nInserisci il numero della porta di partenza: "))
    end_port = int(input("Inserisci il numero della porta finale: "))
except ValueError:
    print("\nErrore: devi inserire numeri interi per il range di porte!")
    exit()

# Verifica del range di porte
if start_port < 1 or end_port > 65535 or start_port > end_port:
    print("\nErrore: range di porte non valido! Assicurati che sia compreso tra 1 e 65535.")
    exit()

# Esegui la scansione
scan_ports(target_ip, start_port, end_port)
