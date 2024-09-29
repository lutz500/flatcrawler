# Flatcrawler

Flatcrawler a web crawler that is used to scrape and manage apartment listings and send notifications via Telegram notifications.

---

# Usage:

## Cronjob Linux:

1. Update packages:

```
sudo apt update
sudo apt upgrade
```

2. Get chromium stable package:

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

3. Install chromium:

```
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
```

4. Check installed 'google-chrome' version:

```
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
```

5. Install venv-requirements:

```
source venv/bin/activate
pip install -r requirements.txt
```

6. Setup crontab:

```
crontabe -e
0 * * * * /path/to/venv/bin/python /path/to/main.py
```
