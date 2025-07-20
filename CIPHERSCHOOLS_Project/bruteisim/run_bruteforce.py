#!/usr/bin/env python3
"""
Brute Force Runner for Multiple Targets
Easy-to-use script to run brute force attacks against various vulnerable web applications
"""

import yaml
import sys
import os
import subprocess
from pathlib import Path

def load_target_configs():
    """Load all available target configurations"""
    configs = {}
    
    # Load predefined targets
    targets_file = Path(__file__).parent / 'targets_config.yaml'
    if targets_file.exists():
        with open(targets_file, 'r') as f:
            configs.update(yaml.safe_load(f))
    
    # Load auto-detected configs if available
    auto_config_file = Path(__file__).parent / 'auto_detected_configs.yaml'
    if auto_config_file.exists():
        with open(auto_config_file, 'r') as f:
            configs.update(yaml.safe_load(f))
    
    return configs

def list_targets(configs):
    """List all available targets"""
    print("\n[+] Available Targets:")
    print("=" * 50)
    
    categories = {
        'Acunetix Test Sites': [],
        'Local Applications': [],
        'Other Targets': []
    }
    
    for name, config in configs.items():
        if 'vulnweb.com' in config.get('url', ''):
            categories['Acunetix Test Sites'].append(name)
        elif 'localhost' in config.get('url', ''):
            categories['Local Applications'].append(name)
        else:
            categories['Other Targets'].append(name)
    
    for category, targets in categories.items():
        if targets:
            print(f"\n{category}:")
            for i, target in enumerate(targets, 1):
                url = configs[target].get('url', 'Unknown')
                username = configs[target].get('username', 'Unknown')
                print(f"  {i}. {target}")
                print(f"     URL: {url}")
                print(f"     Username: {username}")

def create_temp_config(target_name, config):
    """Create a temporary config file for the selected target"""
    temp_config = Path(__file__).parent / f'temp_{target_name}_config.yaml'
    
    with open(temp_config, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    return temp_config

def run_bruteforce(target_name, config, wordlist_choice=None):
    """Run the brute force attack"""
    print(f"\n[+] Starting brute force attack against: {target_name}")
    print(f"[+] Target URL: {config['url']}")
    print(f"[+] Target Username: {config['username']}")
    print("=" * 60)
    
    # Create temporary config
    temp_config = create_temp_config(target_name, config)
    
    try:
        # Build command
        cmd = ['python3', 'bruteisim.py', '--config', str(temp_config)]
        
        if wordlist_choice:
            cmd.extend(['--wordlist', wordlist_choice])
        
        # Run the brute force attack
        print(f"[+] Running command: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=Path(__file__).parent)
        
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
    except Exception as e:
        print(f"[!] Error running attack: {e}")
    finally:
        # Clean up temporary config
        if temp_config.exists():
            temp_config.unlink()

def main():
    print("[+] Brute Force Multi-Target Runner")
    print("[+] For Educational and Testing Purposes Only")
    print("=" * 60)
    
    # Load configurations
    configs = load_target_configs()
    
    if not configs:
        print("[!] No target configurations found!")
        print("[!] Please run target_scanner.py first to detect targets")
        return
    
    # List available targets
    list_targets(configs)
    
    # Get user selection
    print(f"\n[+] Enter target number (1-{len(configs)}) or 'q' to quit: ", end='')
    try:
        choice = input().strip()
        
        if choice.lower() == 'q':
            print("[+] Exiting...")
            return
        
        target_names = list(configs.keys())
        target_index = int(choice) - 1
        
        if target_index < 0 or target_index >= len(target_names):
            print("[!] Invalid selection!")
            return
        
        target_name = target_names[target_index]
        config = configs[target_name]
        
        # Ask for wordlist choice
        print(f"\n[+] Wordlist options for {target_name}:")
        print("1. passwords.txt (default)")
        print("2. common_passwords.txt")
        print("3. password_libraries/10k_common.txt")
        print("4. built-in passwords")
        print("5. Enter custom path")
        
        wordlist_choice = input("\nEnter choice (1-5) or press Enter for default (1): ").strip()
        
        if wordlist_choice == "2":
            wordlist_choice = "common_passwords.txt"
        elif wordlist_choice == "3":
            wordlist_choice = "password_libraries/10k_common.txt"
        elif wordlist_choice == "4":
            wordlist_choice = "builtin"
        elif wordlist_choice == "5":
            wordlist_choice = input("Enter path to password list file: ").strip()
        else:
            wordlist_choice = "passwords.txt"
        
        # Run the attack
        run_bruteforce(target_name, config, wordlist_choice)
        
    except ValueError:
        print("[!] Invalid input!")
    except KeyboardInterrupt:
        print("\n[+] Exiting...")

if __name__ == "__main__":
    main() 