import requests
import time
from typing import List, Optional, Dict, Union, Any

def read_proxies_from_file(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip() and len(line.strip().split(':')) == 4]
    except FileNotFoundError:
        return []

def configure_proxy(proxy_str: str) -> Dict[str, str]:
    try:
        user, password, host, port = proxy_str.split(':')
        proxy_url = f'https://{user}:{password}@{host}:{port}'
        return {'https': proxy_url}
    except ValueError:
        return {}

def test_proxy(proxies: Dict[str, str]) -> bool:
    try:
        response = requests.get('https://api.mojang.com', proxies=proxies, timeout=5)
        return response.status_code == 200
    except:
        return False

def check_username_availability(username: str, proxies_list: Optional[List[str]] = None) -> bool:
    if not proxies_list:
        proxies_list = read_proxies_from_file('proxies.txt')
    
    current_proxy = None
    proxy_index = 0
    retry_count = 0
    max_retries = 3
    proxy_connected = False

    while retry_count < max_retries:
        try:
            # Configure proxy if available
            proxies = {}
            if proxies_list:
                current_proxy = proxies_list[proxy_index]
                proxies = configure_proxy(current_proxy)
                if not test_proxy(proxies):
                    log_action(f"Proxy {proxy_index + 1} failed, trying next")
                    proxy_index = (proxy_index + 1) % len(proxies_list)
                    retry_count += 1
                    continue
                if not proxy_connected:
                    print("Proxy successfully connected")
                    proxy_connected = True

            url = f'https://api.mojang.com/users/profiles/minecraft/{username}'
            start_time = time.perf_counter()
            response = requests.get(url, proxies=proxies if proxies else None, timeout=10)
            end_time = time.perf_counter()
            response_time = int((end_time - start_time) * 1000)  # Convert to milliseconds
            log_action(f"API response for {username}: {response.text}")

            if response.status_code == 429:
                log_action("Rate limit reached, switching proxy or waiting")
                if proxies_list and proxy_index < len(proxies_list) - 1:
                    proxy_index = (proxy_index + 1) % len(proxies_list)
                    print(f"Rate limit reached. Switching to next proxy...")
                    retry_count += 1
                    continue
                else:
                    print(f"Rate limit reached. Waiting 600 seconds before retrying...")
                    time.sleep(600)
                    retry_count += 1
                    if proxies_list:
                        proxy_index = 0  # Reset to first proxy after waiting
                    continue

            if response.status_code in [200, 204, 404]:
                data = response.json() if response.content else {}
                
                if ('errorMessage' in data and 'Couldn\'t find any profile with name' in data['errorMessage']) or 'path' in data:
                    write_available_username(username)
                    log_action(f"Username {username} is available!")
                    print(f"Username {username} is available! ({response_time}ms)")
                    return True
                
                log_action(f'Username {username} is already taken')
                print(f'Username {username} is already taken ({response_time}ms)')
                return False

            log_action(f"Unexpected status code: {response.status_code}")
            print(f"Unexpected status code: {response.status_code}")
            return False

        except Exception as e:
            log_action(f"Error checking {username}: {str(e)}")
            if proxies_list:
                proxy_index = (proxy_index + 1) % len(proxies_list)
            retry_count += 1

    return False

def log_action(action: str) -> None:
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")

def read_words_from_file(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r') as file:
            return [word.strip() for word in file.readlines() if 3 <= len(word.strip()) <= 5]
    except FileNotFoundError:
        return []

def generate_combinations() -> List[str]:
    from itertools import product
    import string
    characters = string.ascii_letters + string.digits
    return [''.join(comb) for comb in product(characters, repeat=3)]

def write_available_username(username: str) -> None:
    with open('available_usernames.txt', 'a') as file:
        file.write(f"{username}\n")

def main() -> None:
    log_action("Script started")
    while True:
        print("\n--- Main Menu ---")
        choice = input("Choose option:\n1. 3 character combinations\n2. Words from files\n3. Manual check\nOr directly enter a username: ")
        log_action(f"User choice: {choice}")

        if choice in ['1', '2', '3']:
            if choice == '1':
                usernames_to_check = generate_combinations()
                log_action("Generated combinations of 3 characters")
                
                for username in usernames_to_check:
                    if not check_username_availability(username):
                        continue
                
            elif choice == '2':
                file_choice = input("Choose file: 1 for words.txt, 2 for francais.txt: ")
                log_action(f"File choice: {file_choice}")
                
                file_path = 'words.txt' if file_choice == '1' else 'francais.txt'
                words = read_words_from_file(file_path)
                if not words:
                    print(f"Error reading {file_path}")
                    continue
                
                for username in words:
                    if not check_username_availability(username):
                        continue
                
            elif choice == '3':
                while True:
                    username = input("Enter username to check: ")
                    available = check_username_availability(username)
                    print(f"\nResult: {'Available' if available else 'Unavailable'}")
                    
                    if input("Check another username? (y/n) ").lower() != 'y':
                        break
                continue
            
            if input("Return to menu? (y/n) ").lower() != 'y':
                break
        else:
            username = choice
            available = check_username_availability(username)
            print(f"\nResult: {'Available' if available else 'Unavailable'}")

if __name__ == '__main__':
    main()