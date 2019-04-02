Auto scrapping from Tableau using Selenium.
1) Scrapper auto updates csv file with latest data from Trailhead.
2) Google sheets auto retrieves the data from the csv file every 24 hours.
3) Dashboard stored in Tableau Public is connected to the Google sheets, will update whenever the "Request Update" button is clicked. 
4) Selenium runs in the background as a cronjob to auto log in to your Tableau account and navigates to click on the "Request Update" button on a periodic basis to refresh the dashboard with updated figures. All these are run in the background using headless-chrome.
