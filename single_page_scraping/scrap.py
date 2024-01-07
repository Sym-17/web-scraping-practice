import requests
from bs4 import BeautifulSoup
import csv

def fetch_data(url: str):
    return requests.get(url)
        
req = fetch_data(url='https://www.scrapethissite.com/pages/simple/')

soup = BeautifulSoup(req.content, "html.parser")

# Open a csv file with the first row (w = write mode)
"""
-> Here encoding="utf-8" is not used previously. Used to solve this error:
-> UnicodeEncodeError: 'charmap' codec can't encode character '\u015f' in position 11: character maps to <undefined>
"""
with open('single_page_scraping/data.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Capital', 'Population', 'Area'])

for country in soup.find_all(class_ = "country"):
    name = country.find(class_ = 'country-name').get_text().strip() #Striped for white space
    capital = country.find(class_ ="country-capital").get_text()
    population = country.find(class_ ="country-population").get_text()
    area = country.find(class_ ="country-area").get_text()

    # Open the existing file and add new row (a = append mode; write if not exit)
    with open('single_page_scraping/data.csv', 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([name, capital, population, area])