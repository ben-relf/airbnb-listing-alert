# airbnb-listing-alert
No accomodation or only over-priced rubbish available for when you need?
Get alerted when new listings appear on Airbnb.

Uses Selenium and BeautifulSoup for page scraping
Email for notifications through gmail.

Can be adjusted for other sites. You just need to find the appropriate html tags to identify the list, list item and name.

Note: Airbnb can change the tags at any time which would break the script.

## Requirements
* Python 3
* Chrome Webdriver - Can be downloaded from: https://chromedriver.chromium.org/downloads
* Google account for email notifications. Recommend setting up new account on google as you will need allow 'less secure apps' to allow this authentication to work. 

## Install
* Create a Python Virtual Environment
```bash
python -m venv airbnb-listing-alert
```
* Activate the virtual environment
```bash
airbnb-listing-alert\Scripts\activate.bat
```
* Upgrade pip
```bash
python -m pip install --upgrade pip
```
* Install from requirements file
```bash
python -m pip install -r requirements.txt
```

## Usage
- Update config
    - Set path to chromedriver.
    - Set gmail settings
    - Search on Airbnb using the required criteria. Save the URL to config.

```bash
python airbnb-listing-alert.py
```

Schedule using cron or windows task manager.