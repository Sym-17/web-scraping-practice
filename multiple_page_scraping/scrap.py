"""
This is actually almost same with single page scraping;
but the main difference is:
    -> Just find the total page numbers list from the HTML
    -> Iterate through the list
"""

import requests
from bs4 import BeautifulSoup
import csv

def fetch_data(url: str):
    return requests.get(url)

req = fetch_data(url='https://www.scrapethissite.com/pages/forms/')
        
soup = BeautifulSoup(req.content, "html.parser")

total_page_list = soup.find(class_ = "pagination")

with open('multiple_page_scraping/hockey_muliple_pages_file.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['Team Name', 'Year', 'Wins', 'Losses', 'OT Losses', 'Win %', 'GF', 'GA', '+/-'])

# page number will be used for dynamically hit the URL
page_number = 1

for li in total_page_list.find_all('li'):

    req = fetch_data(url=f'https://www.scrapethissite.com/pages/forms/?page_num={page_number}')
    soup = BeautifulSoup(req.content, "html.parser")

    for each_team in soup.find_all(class_ = "team"):
        team_name = each_team.find(class_ = "name").get_text().strip()
        year = each_team.find(class_ = "year").get_text().strip()
        wins = each_team.find(class_ = "wins").get_text().strip()
        losses = each_team.find(class_ = "losses").get_text().strip()
        ot_losses = each_team.find(class_ = "ot-losses").get_text().strip()
        win_percent = each_team.find(class_ = "pct").get_text().strip()
        gf = each_team.find(class_ = "gf").get_text().strip()
        ga = each_team.find(class_ = "ga").get_text().strip()
        plus_minus = each_team.find(class_ = "diff").get_text().strip()

        print(team_name, year, wins, losses, ot_losses, win_percent, gf, ga, plus_minus)

        # Open the existing file and add new row (a = append mode; write if not exit)
        with open('multiple_page_scraping/hockey_muliple_pages_file.csv', 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([team_name, year, wins, losses, ot_losses, win_percent, gf, ga, plus_minus])

    page_number += 1