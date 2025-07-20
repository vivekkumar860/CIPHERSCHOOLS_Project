# User Guide: Brute Force Config Generator & Tool

## Quickstart: Run from Terminal or CMD

1. **Clone or download the project:**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
   Or download and extract the ZIP, then open a terminal in the project folder.

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Generate a config file:**
   - Open `webui/index.html` in your browser
   - Fill out the form and click "Download Config YAML"

4. **Run the brute force tool:**
   ```bash
   cd bruteisim
   python3 bruteisim.py --config config.yaml
   ```

---

## Overview
This project provides:
- A **web-based UI** (HTML/JS) for generating brute force config files (hostable on GitHub Pages or run locally)
- A **Python brute force tool** to run attacks using the generated config

---

## 1. How to Run This Project on Your Personal Computer

### Step 1: Download or Clone the Project
- Download the ZIP from GitHub and extract it, or clone with:
  ```bash
  git clone <your-repo-url>
  cd <repo-folder>
  ```

### Step 2: Use the Web UI to Generate a Config
- Open the file `webui/index.html` in your web browser (double-click or right-click > Open With > Browser)
- Select a target and customize the config as needed
- Click **Download Config YAML** to save `config.yaml`

### Step 3: Install Python and Dependencies
- Make sure you have Python 3.x installed
- Open a terminal in the project folder
- Install dependencies:
  ```bash
  pip3 install -r requirements.txt
  ```

### Step 4: Run the Brute Force Tool
- Move your downloaded `config.yaml` into the `bruteisim/` folder (or specify its path)
- In the terminal, run:
  ```bash
  cd bruteisim
  python3 bruteisim.py --config config.yaml
  ```
- Follow the prompts and view results in the terminal

---

## 2. Using the Web UI (Config Generator)

### What is it?
A modern, user-friendly web page for creating config files for the brute force tool. No backend required!

### How to Use
1. **Open the Web UI**
   - If running locally: Open `webui/index.html` in your browser
   - If hosted (e.g., GitHub Pages): Visit your published URL

2. **Select a Target**
   - Choose from the dropdown (e.g., Acunetix PHP, DVWA, etc.)
   - Fields will auto-fill with recommended values

3. **Customize Settings**
   - Change username, field names, indicators, threads, etc. as needed

4. **Download Config**
   - Click "Download Config YAML" to save `config.yaml` to your computer

5. **Follow the Instructions**
   - The page shows how to use the config with the Python tool

---

## 3. Running the Python Brute Force Tool

### Prerequisites
- Python 3.x installed
- Required packages: `requests`, `colorama`, `PyYAML`
  - Install with: `pip3 install -r requirements.txt`

### How to Run
1. Place your `config.yaml` (from the web UI) in the `bruteisim/` directory
2. Open a terminal and navigate to the project folder
3. Run:
   ```bash
   python3 bruteisim.py --config config.yaml
   ```
4. Follow the prompts and view results in the terminal

---

## 4. Deploying the Web UI on GitHub Pages

1. **Push your project to GitHub**
2. Go to your repo settings > Pages
3. Set source to `main` branch and `/webui` folder
4. Save and visit the provided URL (e.g., `https://<username>.github.io/<repo>/webui/`)

---

## 5. FAQ

**Q: Can I run brute force attacks from the browser?**
- No. Browsers cannot run Python or make cross-origin POSTs to arbitrary sites. The web UI is for config generation only.

**Q: Can I add more targets?**
- Yes! Edit `main.js` in `webui/` and add to the `targets` array.

**Q: Can I use my own wordlists?**
- Yes! Place your wordlist in the project and specify its path in the config or CLI.

**Q: Is this legal?**
- Only use this tool on systems you own or have explicit permission to test. For educational and ethical hacking purposes only.

---

## 6. Troubleshooting
- **Web UI not working on GitHub Pages?**
  - Make sure all files are in the `/webui` folder and the source is set correctly in repo settings.
- **Python errors about missing modules?**
  - Run `pip3 install -r requirements.txt` in your project directory.
- **No results or always failing?**
  - Double-check your config values and target accessibility.

---

## 7. Contributing
- Pull requests welcome for new features, targets, or UI improvements!

---

## 8. License
- For educational use only. Use responsibly and ethically. 