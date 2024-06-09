from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")

# Setup Selenium WebDriver
driver_path = r'C:\Users\asus\Desktop\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options= chrome_options)

movies = pd.DataFrame({'id': [], 'Name': [], 'Year':[]})

page_number = 1
entry_number = 1

username = 'hannnahhh'
number_of_pages = 3

url = f'https://letterboxd.com/{username}/films/'
driver.get(url)
time.sleep(5)

print('starting download...')

movies = pd.DataFrame(columns=['id', 'Name', 'Release_Year'])
while (page_number <= number_of_pages):
    user_watchlist_url = f'https://letterboxd.com/{username}/films/page/{page_number}/'
    driver.get(user_watchlist_url)
    time.sleep(10)
    try:
        # Wait for the page to load and find the movie elements
        movie_posters = driver.find_elements(By.XPATH, "//div[contains(@class, '{}')]".format('react-component poster film-poster'))
        for movie in movie_posters:
            movie_id = movie.get_attribute('data-film-id')
            movie_name = movie.get_attribute('data-film-name')
            movie_release_year = movie.get_attribute('data-film-release-year')
            movies.loc[-1] = [movie_id, movie_name, movie_release_year]  # adding a row
            movies.index = movies.index + 1  # shifting index
            movies = movies.sort_index()
                
    except Exception as e:
        print('an error accured in page %i with exception %s' %(page_number, e))
        break
        
    print('downloaded data from page', page_number)
    page_number += 1
        
print('finished download.')

movies.to_csv('hannah-watched.csv', index=False)
driver.quit()