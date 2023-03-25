# Zillow Rental Data Scraper
This is a Python script that uses Beautiful Soup and Selenium to scrape rental data from Zillow for a given location and price range, and then adds the data to a Google Sheets spreadsheet via a Google Form.

## Getting Started
To use this script, you'll need to have Python 3 installed, as well as the following packages:

- BeautifulSoup
- Selenium

You'll also need to create a Google Form with the following fields:

- Address
- Price
- URL

## How it Works
The script requires the user to manually select the location and filters on Zillow's website and then copy the URL link and paste it into the script. It then uses Selenium to automate the process of navigating to the Zillow website and scraping the data.

Beautiful Soup is used to parse the HTML and extract the relevant data for each rental property, including the address, price, and URL. The data is then added to a list.

Finally, the script uses Selenium to automate the process of filling out the Google Form with the rental data.

## Usage
To use the script, simply run python main.py after you have completed the above mentioned steps and configured the file pathto your browser and chrome driver. The script will then scrape the data and add it to the Google Form. From the google form, you can create a Google Sheet from the submitted responses directly.

## Selenium Automation Preview
![2020-08-25_15-50-47-7e40268135497ea3e84762091f48779d](https://user-images.githubusercontent.com/94699055/227706712-858bae2c-8351-4669-8bc4-3c667b566c23.gif)

## Saved Response in Google Spreadsheet
![image](https://user-images.githubusercontent.com/94699055/227706820-b1b4e0f6-3f9d-49f0-9701-523751c7fd06.png)
