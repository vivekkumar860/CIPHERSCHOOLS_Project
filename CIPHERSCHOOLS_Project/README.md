# CIPHERSCHOOLS MiniProject: Advanced Brute-Force Login Script

## Description
This project demonstrates an advanced brute-force login script written in Python with sophisticated features for security research and penetration testing. It includes password library management, smart wordlist generation, and advanced attack strategies.

## Structure
- `bruteisim/bruteisim.py`: Basic brute-force script
- `bruteisim/advanced_brute_force.py`: Advanced brute-force with smart features
- `bruteisim/password_manager.py`: Password library management system
- `bruteisim/config.yaml`: Configuration file
- `bruteisim/passwords.txt`: Sample password list
- `bruteisim/common_passwords.txt`: Extended password list
- `requirements.txt`: Python dependencies
- `README.md`: This documentation

## Advanced Features

### 🔥 **Password Library Management**
- **Automatic Downloads:** Download popular password libraries (RockYou, SecLists, etc.)
- **Library Management:** List, download, and manage password libraries
- **Custom Wordlists:** Create custom wordlists from multiple sources
- **Statistics:** Get detailed statistics for password libraries

### 🧠 **Smart Wordlist Generation**
- **Password Mutations:** Automatic generation of password variations
- **Pattern-Based:** Generate passwords based on common patterns
- **Target-Specific:** Create wordlists based on target information
- **Intelligent Combinations:** Combine multiple strategies

### ⚡ **Advanced Attack Modes**
- **Multi-threading:** Parallel password attempts for speed
- **CAPTCHA Detection:** Automatic detection and handling of CAPTCHAs
- **Rate Limiting:** Configurable delays to avoid detection
- **Proxy Support:** Use proxies for anonymity
- **Custom User-Agents:** Spoof browser user agents

### 🛡️ **Robust Detection**
- **Success Indicators:** Custom text/regex for success detection
- **Failure Indicators:** Detect explicit failure messages
- **Redirect Handling:** Automatic redirect detection
- **Error Handling:** Graceful error recovery

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Basic Brute-Force
```bash
python3 bruteisim/bruteisim.py --config bruteisim/config.yaml
```

### Advanced Brute-Force with Smart Features
```bash
python3 bruteisim/advanced_brute_force.py --url http://target.com/login --username admin --smart
```

### Password Library Management

#### List Available Libraries
```bash
python3 bruteisim/password_manager.py list
```

#### Download a Library
```bash
python3 bruteisim/password_manager.py download --library 10k_common
```

#### Get Library Statistics
```bash
python3 bruteisim/password_manager.py stats --library 10k_common
```

#### Create Custom Wordlist
```bash
python3 bruteisim/password_manager.py create --output my_wordlist --libraries 10k_common darkweb --max-passwords 5000
```

## Available Password Libraries

| Library | Description | Size |
|---------|-------------|------|
| `rockyou` | RockYou password leak (14M passwords) | ~134 MB |
| `10k_common` | 10K most common passwords | ~100 KB |
| `100k_common` | 100K most common passwords | ~1 MB |
| `darkweb` | Dark web password dump (10K) | ~100 KB |
| `crackstation` | CrackStation human-only passwords | ~50 MB |

## Advanced Configuration

### Smart Wordlist Generation
The advanced script can generate intelligent wordlists based on:
- **Username variations** (username123, username2023, etc.)
- **Company names** (if known)
- **Common password mutations** (substitutions, suffixes, prefixes)
- **Pattern-based passwords** (numeric, alphabetic, alphanumeric)

### Password Mutations
The system automatically generates variations like:
- `password` → `p@ssw0rd`, `password123`, `123password`
- `admin` → `@dm1n`, `admin123`, `admin2023`
- `test` → `t3st`, `test123`, `test!`

### Attack Strategies
1. **Basic Attack:** Use provided wordlist
2. **Smart Attack:** Generate intelligent wordlist
3. **Mutation Attack:** Generate variations of common passwords
4. **Pattern Attack:** Generate passwords based on patterns
5. **Hybrid Attack:** Combine multiple strategies

## Configuration Examples

### Basic Config (config.yaml)
```yaml
url: "http://testphp.vulnweb.com/userinfo.php"
username: "test"
username_field: "uname"
password_field: "pass"
success_indicator: "User Info"
threads: 8
debug: true
```

### Advanced Config with Smart Features
```yaml
url: "http://target.com/login"
username: "admin"
username_field: "username"
password_field: "password"
success_indicator: "Welcome"
failure_indicator: "Invalid credentials"
threads: 16
delay: 0.1
smart: true
```

## Command-Line Options

### Basic Script
- `--url`: Target login URL
- `--username`: Username to test
- `--wordlist`: Path to password file
- `--config`: YAML config file
- `--threads`: Number of threads (default: 4)
- `--debug`: Enable debug output

### Advanced Script
- `--smart`: Use smart wordlist generation
- `--delay`: Delay between requests
- `--proxy`: Use proxy for requests
- `--user-agent`: Custom user agent
- All basic options plus advanced features

### Password Manager
- `list`: List available libraries
- `download --library`: Download specific library
- `stats --library`: Get library statistics
- `create --output`: Create custom wordlist

## Examples

### Download and Use RockYou
```bash
# Download RockYou library
python3 bruteisim/password_manager.py download --library rockyou

# Use in attack
python3 bruteisim/advanced_brute_force.py --url http://target.com/login --username admin --wordlist password_libraries/rockyou.txt
```

### Smart Attack with Mutations
```bash
python3 bruteisim/advanced_brute_force.py --url http://target.com/login --username admin --smart --threads 16
```

### Custom Wordlist Attack
```bash
# Create custom wordlist
python3 bruteisim/password_manager.py create --output my_attack --libraries 10k_common darkweb --max-passwords 10000

# Use custom wordlist
python3 bruteisim/advanced_brute_force.py --url http://target.com/login --username admin --wordlist password_libraries/my_attack.txt
```

## Ethical Disclaimer
**This script is for educational and authorized penetration testing purposes only.**
Do not use this tool against systems without explicit written permission. Unauthorized use is illegal and unethical.

## Advanced Features Summary

### 🔧 **Technical Capabilities**
- Multi-threaded attacks with configurable concurrency
- Automatic CAPTCHA and lockout detection
- Proxy and user-agent spoofing
- Comprehensive logging and debugging
- Graceful interrupt handling

### 📊 **Intelligence Features**
- Smart wordlist generation based on target analysis
- Password mutation algorithms
- Pattern-based password generation
- Library management and statistics

### 🛡️ **Security Features**
- Rate limiting to avoid detection
- Configurable timeouts and delays
- Error handling and recovery
- Thread-safe operations

This advanced brute-force framework provides professional-grade capabilities for security research and penetration testing while maintaining ethical usage guidelines. 