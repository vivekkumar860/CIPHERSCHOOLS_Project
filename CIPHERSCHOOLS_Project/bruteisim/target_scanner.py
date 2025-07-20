#!/usr/bin/env python3
"""
Target Scanner for Brute Force Testing
Automatically detects login forms and tests configurations for various vulnerable web applications
"""

import requests
import yaml
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

class TargetScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scan_target(self, base_url):
        """Scan a target website to find login forms and test configurations"""
        print(f"\n[+] Scanning target: {base_url}")
        
        try:
            # Get the main page
            response = self.session.get(base_url, timeout=10)
            if response.status_code != 200:
                print(f"[!] Failed to access {base_url}")
                return None
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all forms
            forms = soup.find_all('form')
            login_forms = []
            
            for form in forms:
                if self.is_login_form(form):
                    login_forms.append(form)
            
            if not login_forms:
                print(f"[!] No login forms found on {base_url}")
                return None
            
            print(f"[+] Found {len(login_forms)} potential login form(s)")
            
            # Test each login form
            for i, form in enumerate(login_forms):
                print(f"\n[+] Testing login form {i+1}:")
                config = self.analyze_login_form(form, base_url)
                if config:
                    return config
            
            return None
            
        except Exception as e:
            print(f"[!] Error scanning {base_url}: {e}")
            return None
    
    def is_login_form(self, form):
        """Check if a form is likely a login form"""
        form_text = form.get_text().lower()
        form_action = form.get('action', '').lower()
        
        # Check for login-related keywords
        login_keywords = ['login', 'signin', 'auth', 'user', 'password']
        return any(keyword in form_text or keyword in form_action for keyword in login_keywords)
    
    def analyze_login_form(self, form, base_url):
        """Analyze a login form and create a configuration"""
        action = form.get('action', '')
        method = form.get('method', 'get').lower()
        
        # Build full URL
        if action.startswith('http'):
            form_url = action
        else:
            form_url = urljoin(base_url, action)
        
        # Find input fields
        inputs = form.find_all('input')
        username_field = None
        password_field = None
        
        for inp in inputs:
            input_type = inp.get('type', '').lower()
            input_name = inp.get('name', '')
            
            if input_type == 'text' or input_type == 'email':
                if not username_field:
                    username_field = input_name
            elif input_type == 'password':
                password_field = input_name
        
        if not username_field or not password_field:
            print(f"[!] Could not identify username/password fields")
            return None
        
        print(f"[+] Form URL: {form_url}")
        print(f"[+] Username field: {username_field}")
        print(f"[+] Password field: {password_field}")
        
        # Test with common credentials
        config = self.test_login_config(form_url, username_field, password_field, method)
        return config
    
    def test_login_config(self, url, username_field, password_field, method):
        """Test login configuration with common credentials"""
        test_credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('test', 'test'),
            ('user', 'password'),
            ('root', 'root'),
            ('admin', '123456'),
            ('admin', 'admin123')
        ]
        
        print(f"[+] Testing login with common credentials...")
        
        for username, password in test_credentials:
            try:
                data = {username_field: username, password_field: password}
                
                if method == 'post':
                    response = self.session.post(url, data=data, timeout=10)
                else:
                    response = self.session.get(url, params=data, timeout=10)
                
                # Analyze response for success/failure indicators
                success_indicators = self.detect_success_indicators(response)
                failure_indicators = self.detect_failure_indicators(response)
                
                if success_indicators:
                    print(f"[+] SUCCESS with {username}:{password}")
                    print(f"[+] Success indicators: {success_indicators}")
                    print(f"[+] Failure indicators: {failure_indicators}")
                    
                    return {
                        'url': url,
                        'username': username,
                        'username_field': username_field,
                        'password_field': password_field,
                        'success_indicator': success_indicators[0] if success_indicators else 'welcome',
                        'failure_indicator': failure_indicators[0] if failure_indicators else 'invalid',
                        'threads': 4,
                        'timeout': 10,
                        'delay': 0,
                        'progress_interval': 10
                    }
                
                time.sleep(0.5)  # Small delay between requests
                
            except Exception as e:
                print(f"[!] Error testing {username}:{password} - {e}")
                continue
        
        print(f"[!] No successful login found with common credentials")
        return None
    
    def detect_success_indicators(self, response):
        """Detect potential success indicators in response"""
        text = response.text.lower()
        success_patterns = [
            'welcome', 'dashboard', 'profile', 'account', 'logged in',
            'success', 'authenticated', 'user info', 'my account'
        ]
        
        indicators = []
        for pattern in success_patterns:
            if pattern in text:
                indicators.append(pattern)
        
        return indicators
    
    def detect_failure_indicators(self, response):
        """Detect potential failure indicators in response"""
        text = response.text.lower()
        failure_patterns = [
            'invalid', 'failed', 'incorrect', 'wrong', 'error',
            'not found', 'denied', 'unauthorized', 'must login'
        ]
        
        indicators = []
        for pattern in failure_patterns:
            if pattern in text:
                indicators.append(pattern)
        
        return indicators

def main():
    # List of known vulnerable web applications
    targets = {
        'testphp.vulnweb.com': 'http://testphp.vulnweb.com/',
        'testhtml5.vulnweb.com': 'http://testhtml5.vulnweb.com/',
        'testasp.vulnweb.com': 'http://testasp.vulnweb.com/',
        'testaspnet.vulnweb.com': 'http://testaspnet.vulnweb.com/',
        'rest.vulnweb.com': 'http://rest.vulnweb.com/'
    }
    
    scanner = TargetScanner()
    configurations = {}
    
    print("[+] Target Scanner for Brute Force Testing")
    print("[+] Scanning known vulnerable web applications...")
    
    for name, url in targets.items():
        config = scanner.scan_target(url)
        if config:
            configurations[name] = config
            print(f"\n[+] Configuration for {name}:")
            print(yaml.dump(config, default_flow_style=False))
    
    # Save configurations
    if configurations:
        with open('auto_detected_configs.yaml', 'w') as f:
            yaml.dump(configurations, f, default_flow_style=False)
        print(f"\n[+] Saved {len(configurations)} configurations to auto_detected_configs.yaml")
    
    print(f"\n[+] Scan complete. Found {len(configurations)} working configurations.")

if __name__ == "__main__":
    main() 