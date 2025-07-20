# Brute Force Multi-Target Testing Tool

This project provides a comprehensive brute force testing tool that can be used against various vulnerable web applications for educational and security testing purposes.

## 🎯 Supported Targets

### 1. Acunetix Vulnerable Web Applications
These are publicly available test sites provided by Acunetix:

- **testphp.vulnweb.com** - PHP/MySQL application
- **testhtml5.vulnweb.com** - HTML5 application  
- **testasp.vulnweb.com** - ASP application
- **testaspnet.vulnweb.com** - ASP.NET application
- **rest.vulnweb.com** - REST API testing

### 2. Local Vulnerable Applications
For local testing (requires setup):

- **DVWA** (Damn Vulnerable Web Application)
- **OWASP Juice Shop**
- **OWASP WebGoat**
- **bWAPP** (Buggy Web Application)

## 🚀 Quick Start

### Method 1: Using the Multi-Target Runner
```bash
cd CIPHERSCHOOLS_MiniProject/bruteisim
python3 run_bruteforce.py
```

This will show you a list of available targets and let you choose which one to attack.

### Method 2: Direct Configuration
```bash
cd CIPHERSCHOOLS_MiniProject/bruteisim
python3 bruteisim.py --config config.yaml
```

### Method 3: Auto-Detection
```bash
cd CIPHERSCHOOLS_MiniProject/bruteisim
python3 target_scanner.py  # First scan for targets
python3 run_bruteforce.py  # Then run attacks
```

## 📋 Target Configurations

### Acunetix PHP Test Site
```yaml
url: "http://testphp.vulnweb.com/userinfo.php"
username: "test"
username_field: "uname"
password_field: "pass"
success_indicator: "John Smith"
failure_indicator: "you must login"
```

**Known Credentials:** `test:test`

### Acunetix HTML5 Test Site
```yaml
url: "http://testhtml5.vulnweb.com/login.php"
username: "admin"
username_field: "username"
password_field: "password"
success_indicator: "welcome"
failure_indicator: "invalid"
```

### DVWA (Local Setup)
```yaml
url: "http://localhost/dvwa/login.php"
username: "admin"
username_field: "username"
password_field: "password"
success_indicator: "Welcome to Damn Vulnerable Web Application"
failure_indicator: "Login failed"
```

**Known Credentials:** `admin:password`

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Install Additional Dependencies for Target Scanner
```bash
pip3 install beautifulsoup4
```

### 3. Set Up Local Vulnerable Applications

#### DVWA Setup
```bash
# Using Docker
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Or download and set up manually
# Visit: https://github.com/digininja/DVWA
```

#### OWASP Juice Shop Setup
```bash
# Using Docker
docker run --rm -p 3000:3000 bkimminich/juice-shop

# Or using Node.js
npm install -g juice-shop
juice-shop
```

#### OWASP WebGoat Setup
```bash
# Using Docker
docker run --rm -p 8080:8080 webgoat/webgoat

# Or download JAR file
# Visit: https://github.com/WebGoat/WebGoat
```

## 📁 File Structure

```
CIPHERSCHOOLS_MiniProject/
├── bruteisim/
│   ├── bruteisim.py              # Main brute force tool
│   ├── config.yaml               # Default configuration
│   ├── targets_config.yaml       # Multiple target configurations
│   ├── target_scanner.py         # Auto-detection script
│   ├── run_bruteforce.py         # Multi-target runner
│   ├── passwords.txt             # Default password list
│   ├── common_passwords.txt      # Common passwords
│   └── password_libraries/
│       └── 10k_common.txt       # Large password dictionary
├── requirements.txt
└── README_MULTI_TARGET.md
```

## 🎮 Usage Examples

### Example 1: Attack testphp.vulnweb.com
```bash
cd CIPHERSCHOOLS_MiniProject/bruteisim
python3 run_bruteforce.py
# Select target 1 (acunetix_php)
# Choose wordlist option
```

### Example 2: Custom Target
```bash
python3 bruteisim.py \
  --url "http://your-target.com/login.php" \
  --username "admin" \
  --username-field "user" \
  --password-field "pass" \
  --success-indicator "welcome" \
  --failure-indicator "invalid" \
  --wordlist "password_libraries/10k_common.txt"
```

### Example 3: Auto-Detect and Attack
```bash
# First, scan for targets
python3 target_scanner.py

# Then run attacks against detected targets
python3 run_bruteforce.py
```

## 🔧 Configuration Options

### Basic Options
- `url`: Target login URL
- `username`: Username to test
- `username_field`: Form field name for username
- `password_field`: Form field name for password
- `success_indicator`: Text indicating successful login
- `failure_indicator`: Text indicating failed login

### Advanced Options
- `threads`: Number of concurrent threads (default: 4)
- `timeout`: Request timeout in seconds (default: 10)
- `delay`: Delay between requests (default: 0)
- `progress_interval`: Progress update frequency (default: 10)

## 📊 Wordlist Options

1. **passwords.txt** - Default small wordlist (43 passwords)
2. **common_passwords.txt** - Common passwords (84 passwords)
3. **password_libraries/10k_common.txt** - Large dictionary (10,000 passwords)
4. **built-in passwords** - Hardcoded common passwords
5. **Custom path** - Your own password file

## ⚠️ Important Notes

### Legal and Ethical Use
- This tool is for **educational purposes only**
- Only test against systems you own or have explicit permission to test
- Many of the listed targets are intentionally vulnerable for learning
- Always follow responsible disclosure practices

### Security Considerations
- The tool includes rate limiting and delays to avoid overwhelming targets
- Use appropriate wordlists for testing
- Monitor network traffic and system resources
- Stop attacks immediately if unexpected behavior occurs

### Performance Tips
- Start with smaller wordlists for testing
- Use appropriate thread counts for your network
- Monitor target response times
- Consider using proxies for large-scale testing

## 🐛 Troubleshooting

### Common Issues

1. **"No login forms found"**
   - Check if the target URL is accessible
   - Verify the target has a login form
   - Try different URLs for the same application

2. **"Invalid credentials" errors**
   - Verify the form field names
   - Check success/failure indicators
   - Test manually with known credentials

3. **Rate limiting/CAPTCHA**
   - Increase delays between requests
   - Reduce thread count
   - Use different User-Agent strings

4. **Connection timeouts**
   - Check network connectivity
   - Increase timeout values
   - Verify target is online

## 📚 Additional Resources

### Vulnerable Web Applications
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [DVWA](http://www.dvwa.co.uk/)
- [bWAPP](http://www.itsecgames.com/)

### Password Lists
- [SecLists](https://github.com/danielmiessler/SecLists)
- [RockYou](https://github.com/brannondorsey/naive-hashcat/releases)
- [Common Passwords](https://github.com/danielmiessler/SecLists/tree/master/Passwords)

### Learning Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web Application Security Testing](https://owasp.org/www-project-web-security-testing-guide/)
- [Brute Force Attack Prevention](https://owasp.org/www-community/attacks/Brute_force_attack)

## 🤝 Contributing

Feel free to contribute by:
- Adding new target configurations
- Improving detection algorithms
- Adding new wordlists
- Enhancing documentation
- Reporting bugs or issues

## 📄 License

This project is for educational purposes only. Use responsibly and ethically. 