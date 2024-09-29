# Flatcrawler

Flatcrawler a web crawler that is used to scrape and manage apartment listings and send notifications via Telegram notifications.

---

# Usage:

## Cronjob Linux:

1. Update packages:

```bash
sudo apt update
sudo apt upgrade
```

2. Get chromium stable package:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

3. Install chromium:

```bash
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
```

4. Check installed 'google-chrome' version:

```bash
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
```

5. Set environment variables: <br />
   Create an `.env` file with the following variables:

```python
TELEGRAM_TOKEN = <TELEGRAM API-TOKEN>
TELEGRAM_CHAT_ID = <TELEGRAM CHAT ID>
TELEGERAM_BOT = <TELGERAM BOT ID
URL_STADTBAU = <URL TO SCRAPE>
```

5. Install venv-requirements:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

6. Setup crontab:

```bash
crontabe -e
0 * * * * /path/to/venv/bin/python /path/to/main.py
```
