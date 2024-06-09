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

movies = pd.read_csv('hannah-watched.csv')
print(movies.head())

page_number = 1
rate_number = 2.5
number_of_pages = 1

username = 'hannnahhh'
url = f'https://letterboxd.com/{username}/films/'
driver.get(url)
time.sleep(5)

print('starting download...')

while (page_number <= number_of_pages):
    user_films_url = f'https://letterboxd.com/{username}/films/rated/{rate_number}/page/{page_number}/'
    driver.get(user_films_url)
    time.sleep(10)
    try:
        # Wait for the page to load and find the movie elements
        movie_posters = driver.find_elements(By.XPATH, "//div[contains(@class, '{}')]".format('react-component poster film-poster'))
        for movie in movie_posters:
            movie_id = movie.get_attribute('data-film-id')
            movie_name = movie.get_attribute('data-film-name')
            print(movie_name)
            movies.loc[movies['Name'] == movie_name, 'user_rate'] = rate_number
                
    except Exception as e:
        print('an error accured in page %i with exception %s' %(page_number, e))
        break
        
    print('downloaded data from page', page_number)
    page_number += 1
        
print('finished download.')

movies.to_csv('hannah-watched.csv', index=False)
driver.quit()