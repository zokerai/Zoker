import os
import json
import time
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from git import Repo  # Requires GitPython (pip install gitpython)

# AI Configuration Files
CONFIG_FILE = "config.json"
MAIN_SCRIPT = "zoker_ai.py"
GITHUB_REPO = "https://github.com/zokerai/Zoker"
GITHUB_LOCAL_PATH = "./zoker_repo"

# Load Settings
def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"learning_speed": "medium", "status": "running", "last_update": "never"}

# Save Settings
def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

# Read its own script
def read_own_code():
    try:
        with open(MAIN_SCRIPT, "r", encoding="utf-8") as file:  # Ensure UTF-8 encoding to avoid decoding issues
            return file.read()
    except FileNotFoundError:
        return "Error: Main script not found."
    except UnicodeDecodeError as e:
        return f"Error: Unicode decode error - {str(e)}"

# Scrape web pages for code improvements
def scrape_code_improvements():
    websites = [
        "https://realpython.com",
        "https://towardsdatascience.com",
        "https://www.geeksforgeeks.org/python-programming-language/",
    ]
    scraped_text = ""

    for site in websites:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            response = requests.get(site, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            scraped_text += soup.get_text()[:1000]  # Scrape the first 1000 characters
            time.sleep(2)  # Prevent too many requests in a short time
        except Exception as e:
            print(f"Error scraping {site}: {e}")
    
    return scraped_text

# Write new improved code
def write_new_code(improvements):
    new_code = f"# AI-Generated Improvements\n\n{improvements}"
    with open(MAIN_SCRIPT, "w", encoding="utf-8") as file:  # Use utf-8 encoding to prevent encoding issues
        file.write(new_code)

# Push updated code to GitHub
def push_to_github():
    if not os.path.exists(GITHUB_LOCAL_PATH):
        Repo.clone_from(GITHUB_REPO, GITHUB_LOCAL_PATH)

    repo = Repo(GITHUB_LOCAL_PATH)
    repo.git.add(MAIN_SCRIPT)
    repo.index.commit("Auto-update: Code improvements from web scraping")
    origin = repo.remote(name="origin")
    origin.push()

# Auto-run updated script
def run_updated_script():
    os.system(f"python {MAIN_SCRIPT}")

# Log AI actions
def log_action(action):
    with open("zoker_log.txt", "a", encoding="utf-8") as file:  # Ensure UTF-8 encoding
        file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}\n")

# Scrape web pages for knowledge (code-focused websites)
def start_learning():
    config = load_config()
    if config["status"] != "running":
        print("AI is paused. Change config to start.")
        return

    print("🔍 Scraping websites for code improvements...")
    improvements = scrape_code_improvements()
    if improvements:
        print(f"Scraped improvements:\n{improvements[:500]}...")  # Print first 500 characters of scraped text
    else:
        print("No improvements found.")
    
    log_action(f"Scraped code improvements:\n{improvements[:500]}...")

# Main AI Loop for Improvement
def auto_improve():
    config = load_config()
    if config["status"] != "running":
        print("AI is paused. Change config to start.")
        return

    print("🔍 Reading AI's own code...")
    code = read_own_code()
    
    print("🛠 Scraping code improvements from the web...")
    improvements = scrape_code_improvements()

    print("💾 Writing new code...")
    write_new_code(improvements)

    print("⬆️ Pushing to GitHub...")
    push_to_github()

    print("🚀 Running updated AI...")
    run_updated_script()

# CLI for controlling the AI
def control_ai():
    while True:
        command = input("\nEnter command (start/stop/status/exit/improve): ").strip().lower()
        if command == "start":
            save_config({"learning_speed": "medium", "status": "running"})
            start_learning()
        elif command == "stop":
            save_config({"status": "paused"})
            print("AI stopped.")
        elif command == "status":
            config = load_config()
            print(f"AI Status: {config['status']}")
        elif command == "improve":
            auto_improve()
        elif command == "exit":
            break
        else:
            print("Invalid command.")

# Run AI Control
control_ai()
