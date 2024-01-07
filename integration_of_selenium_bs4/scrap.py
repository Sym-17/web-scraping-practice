"""
Here we will do these:
    -> Use selenium to "select" some "options" of a page
    -> Get the data by beautiful soap(bs4)
    -> Store data at DB by PostgreSQL
"""

import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import psycopg2

driver = webdriver.Chrome()

driver.get("https://www.olympedia.org/statistics/medal/country")

driver.implicitly_wait(0.5)

# selected_field = driver.find_element(by=By.XPATH, value="/html[1]/body[1]/div[2]/form[1]/select[3]/")
selected_field = driver.find_element(by=By.ID, value="edition_select")
select = Select(selected_field)

select.select_by_visible_text('1896')

time.sleep(3)
       
page_data_after_select = driver.page_source

soup = BeautifulSoup(page_data_after_select, "html.parser")

data = soup.find(class_ = "table table-striped")

# Database connection setup
db_connection = psycopg2.connect(
    host="localhost",
    database="web-scraping-practice",
    user="postgres",
    password="sayem2017",
    port = "5432"
)

# Create a cursor
cursor = db_connection.cursor()    

for each_row in data.find_all('tr'):
    row_data = []
    for each_col in each_row.find_all('td'):
        row_data.append(each_col.get_text())

    if len(row_data)>0:
        cursor.execute("INSERT INTO olympic_data (country_name, country_code, gold, silver, bronze, total) VALUES (%s, %s, %s, %s, %s, %s)", (row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5]))


# Commit the changes and close the database connection
driver.quit()
db_connection.commit()
cursor.close()
db_connection.close()




