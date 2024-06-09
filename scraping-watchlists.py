from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from lxml import html
import time

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")

# Setup Selenium WebDriver
driver_path = r'C:\Users\asus\Desktop\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options= chrome_options)

movies = pd.DataFrame({'id': [], 'Name': [], 'Year':[]})
print('woke up')

for i in range(12):
    # Navigate to the user's watchlist page
    user_watchlist_url = f'https://letterboxd.com/dejbord/watchlist/page/{i+1}/'
    driver.get(user_watchlist_url)
    time.sleep(10)
    print('downloading data from page', i+1)
    try:
        # Wait for the page to load and find the movie elements
        movie_posters = driver.find_elements(By.XPATH, "//div[contains(@class, '{}')]".format('react-component poster film-poster'))
    
        for movie in movie_posters:
            # Extract movie ID, name, and release year
            movie_id = movie.get_attribute('data-film-id')
            movie_name = movie.get_attribute('data-film-name')
            movie_release_year = movie.get_attribute('data-film-release-year')
            movies.loc[-1] = [movie_id, movie_name, movie_release_year]  # adding a row
            movies.index = movies.index + 1  # shifting index
            movies = movies.sort_index()
            
    except:
        print('an error accured')

movies.to_csv('navid-watchlist.csv', index=False)
driver.quit()