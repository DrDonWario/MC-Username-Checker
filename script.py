import requests
import time

# Function to check username availability
def check_username_availability(username, proxies_list=None, current_proxy_index=0):
    proxies = {}
    if proxies_list and current_proxy_index < len(proxies_list):
        try:
            # Format: user:password:host:port
            proxy = proxies_list[current_proxy_index]
            user, password, host, port = proxy.split(':')
            
            # Configure HTTPS proxy
            proxy_url = f'https://{user}:{password}@{host}:{port}'
            proxies = {'https': proxy_url}
            
            # Test connection
            test_url = 'https://api.mojang.com'
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"Proxy {current_proxy_index + 1} connecté en HTTPS.")
                print(f"Configuration proxy: {host}:{port}")
            else:
                print(f"Erreur de connexion au proxy {current_proxy_index + 1}")
                # Try next proxy if available
                if proxies_list and current_proxy_index + 1 < len(proxies_list):
                    print(f"Tentative avec le proxy suivant...")
                    return check_username_availability(username, proxies_list, current_proxy_index + 1)
                return None
                
        except ValueError as e:
            print("Erreur de configuration proxy:")
            print("Format attendu: user:password:host:port")
            print("Exemple: user:pass:1.2.3.4:8080")
            # Try next proxy if available
            if proxies_list and current_proxy_index + 1 < len(proxies_list):
                print(f"Tentative avec le proxy suivant...")
                return check_username_availability(username, proxies_list, current_proxy_index + 1)
            return None
        except Exception as e:
            print(f"Erreur de connexion proxy {current_proxy_index + 1}: {str(e)}")
            # Try next proxy if available
            if proxies_list and current_proxy_index + 1 < len(proxies_list):
                print(f"Tentative avec le proxy suivant...")
                return check_username_availability(username, proxies_list, current_proxy_index + 1)
            return None

    url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
    try:
        response = requests.get(url, proxies=proxies if proxy else None)
        log_action(f"API response for {username}: {response.text}")
        
        if response.status_code == 429:
            log_action("Rate limit atteint (429)")
            print("\nLimite de taux atteinte (429) !")
            print("Options:")
            print("1. Attendre 600 secondes et continuer")
            print("2. Utiliser un proxy")
            print("3. Retourner au menu principal")
            
            choice = input("Choisissez une option (1/2/3): ")
            
            if choice == '1':
                print("\nAttente de 600 secondes...")
                time.sleep(600)
                return check_username_availability(username, proxies_list, current_proxy_index)
            elif choice == '2':
                if not proxies_list:
                    print("\nAucun proxy disponible dans proxies.txt")
                    return None
                # Try next proxy if available
                if current_proxy_index + 1 < len(proxies_list):
                    print(f"\nPassage au proxy suivant...")
                    return check_username_availability(username, proxies_list, current_proxy_index + 1)
                else:
                    print("\nTous les proxies ont été essayés. Retour au premier proxy.")
                    return check_username_availability(username, proxies_list, 0)
            else:
                return None
        
        if response.status_code in [200, 204, 404]:
            data = response.json() if response.content else {}
            
            if 'errorMessage' in data and 'Couldn\'t find any profile with name' in data['errorMessage']:
                write_available_username(username)
                log_action(f"Username {username} est disponible !")
                print(f"Username {username} est disponible !")
                return True
            
            if 'path' in data:
                write_available_username(username)
                log_action(f"Username {username} est disponible !")
                print(f"Username {username} est disponible !")
                return True
            
            log_action(f'Username {username} is already taken')
            print(f'Username {username} is already taken')
            return False
        
        log_action(f"Code de statut inattendu: {response.status_code}")
        print(f"Code de statut inattendu: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        log_action(f"Error checking {username}: {str(e)}")
        print(f"Error checking {username}: {str(e)}")
        pass
    return False

# Function to log actions
def log_action(action):
    with open('logs.txt', 'a') as log_file:
        log_file.write(action + '\n')

# Function to read words from a file
def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        return [word.strip() for word in file.readlines() if 3 <= len(word.strip()) <= 5]

# Function to generate all combinations of 3 characters
def generate_combinations():
    from itertools import product
    import string
    characters = string.ascii_letters + string.digits
    return [''.join(comb) for comb in product(characters, repeat=3)]

# Function to write available usernames to a file
def write_available_username(username):
    with open('available_usernames.txt', 'a') as file:
        file.write(username + '\n')

# Function to read proxies from a file
def read_proxies_from_file(file_path):
    with open(file_path, 'r') as file:
        proxies = []
        for line in file:
            line = line.strip()
            if line and len(line.split(':')) == 4:
                proxies.append(line)
        return proxies

# Main function to check usernames
def main():
    log_action("Script started")
    proxies = read_proxies_from_file('proxies.txt')
    while True:
        print("\n--- Menu Principal ---")
        choice = input("Choisissez l'option :\n1. Combinaisons 3 caractères\n2. Mots depuis fichiers\n3. Vérification manuelle\nOu saisissez directement un pseudo : ")
        log_action(f"User choice: {choice}")

        if choice in ['1', '2', '3']:
            if choice == '1':
                usernames_to_check = generate_combinations()
                log_action("Generated combinations of 3 characters")
                
                # Vérification des pseudos pour l'option 1
                # Automatically use all available proxies
                if proxies:
                    valid_proxies = [proxy for proxy in proxies if len(proxy.split(':')) == 4]
                    if not valid_proxies:
                        print("Format de proxy invalide dans proxies.txt")
                        continue
                    log_action(f"Using {len(valid_proxies)} proxies automatically")
                
                for i, username in enumerate(usernames_to_check):
                    result = check_username_availability(username, valid_proxies if proxies else None)
                    if result is None:
                        break
                
            elif choice == '2':
                file_choice = input("Choisissez le fichier: 1 pour words.txt, 2 pour francais.txt: ")
                log_action(f"File choice: {file_choice}")
                
                if file_choice == '1':
                    words = read_words_from_file('words.txt')
                    log_action("Read words from words.txt")
                elif file_choice == '2':
                    words = read_words_from_file('francais.txt')
                    log_action("Read words from francais.txt")
                else:
                    print("Choix invalide")
                    log_action("Invalid file choice")
                    continue
                    
                usernames_to_check = words
                
                # Vérification des pseudos pour l'option 2
                # Automatically use all available proxies
                if proxies:
                    valid_proxies = [proxy for proxy in proxies if len(proxy.split(':')) == 4]
                    if not valid_proxies:
                        print("Format de proxy invalide dans proxies.txt")
                        continue
                    log_action(f"Using {len(valid_proxies)} proxies automatically")
                
                for i, username in enumerate(usernames_to_check):
                    result = check_username_availability(username, valid_proxies if proxies else None)
                    if result is None:
                        break
                
            elif choice == '3':
                while True:
                    username = input("Entrez le pseudo à vérifier: ")
                    
                    # Automatically use all available proxies
                    valid_proxies = None
                    if proxies:
                        valid_proxies = [proxy for proxy in proxies if len(proxy.split(':')) == 4]
                        if valid_proxies:
                            log_action(f"Using {len(valid_proxies)} proxies automatically")
                        else:
                            print("Format de proxy invalide dans proxies.txt")
                    
                    disponible = check_username_availability(username, valid_proxies)
                    print(f"\nRésultat : {'Disponible' if disponible else 'Indisponible'}")
                    
                    if input("Vérifier un autre pseudo ? (o/n) ").lower() != 'o':
                        break
                continue
            
            if input("Revenir au menu ? (o/n) ").lower() != 'o':
                break
        else:
            # Vérification directe d'un pseudo saisi
            username = choice
            
            # Automatically use all available proxies
            valid_proxies = None
            if proxies:
                valid_proxies = [proxy for proxy in proxies if len(proxy.split(':')) == 4]
                if valid_proxies:
                    log_action(f"Using {len(valid_proxies)} proxies automatically")
                else:
                    print("Format de proxy invalide dans proxies.txt")
                    continue

            disponible = check_username_availability(username, valid_proxies)
            print(f"\nRésultat : {'Disponible' if disponible else 'Indisponible'}")


if __name__ == '__main__':
    main()