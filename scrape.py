#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import datetime, time
import numpy as np
import click
import selenium


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


#url = 'www.expedia.com'
flight_tab = "//button[ @id='tab-flight-tab-hp']"
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"
depature_country = "//input[@id='flight-origin-hp-flight']"
arrival_country = "//input[@id='flight-destination-hp-flight']"
search_tab = "//button[@class='btn-primary btn-action gcw-submit']"
country_list = [depature_country,arrival_country]



def ticket_chooser(ticket):
    try:
        ticket_type = driver.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        print(e)


def select_country(country_list,dep_cou,arr_cou):
    try:
        for country in country_list:
            if country == depature_country:
                fly_from = driver.find_element_by_xpath(country)
                time.sleep(1)
                fly_from.clear()
                time.sleep(1)
                fly_from.send_keys(dep_cou)
                time.sleep(0.5)
                first_item = driver.find_element_by_xpath("//a[@id='aria-option-0']")
                time.sleep(1)
                first_item.click()
            elif country == arrival_country:
                fly_to = driver.find_element_by_xpath(country)
                time.sleep(1)
                fly_to.clear()
                time.sleep(1)
                fly_to.send_keys(" " + arr_cou)
                time.sleep(0.5)
                second_item = driver.find_element_by_xpath("//a[@id='aria-option-0']")
                time.sleep(1)
                second_item.click()
            else:
                raise ValueError
    except Exception as e:
        print(e)


def dep_date(month, day, year):
    dep_date_button = driver.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)


def return_date(month,day,year):
    dep_date_button = driver.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
    dep_date_button.clear()
    for _ in range(10):
        dep_date_button.send_keys(selenium.webdriver.common.keys.Keys.BACK_SPACE)
    time.sleep(1)
    dep_date_button.send_keys(month + '/' + day + '/' + year)
    dep_date_button.click()

def search(search):
    search_button = driver.find_element_by_xpath(search)
    search_button.click()

def flight(flight):
    flight_tab = driver.find_element_by_xpath(flight)
    flight_tab.click()
    
def get_url(url):
    driver.get(url)
    
df = pd.DataFrame()
def compile_data():
    #departure times
    dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    #arrival times
    arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]
    #airline name
    airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]
    empty = airlines_list.pop(0)
    #prices
    prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text.split('$')[1] for value in prices]
    #durations
    durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]
    #stops
    stops = driver.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]
    #layovers
    layovers = driver.find_elements_by_xpath("//span[@data-test-id='layover-info']")
    layovers_list = [value.text for value in layovers]
    
    rating = driver.find_elements_by_xpath("//a[@data-click-handler='omnitureClickHandler']")
    rating_list = [value.text for value in rating]
    
    joined_list = [dep_times_list,arr_times_list,airlines_list,price_list,durations_list,stops_list,layovers_list\
                  ,rating_list]
    columns = ['departure_time','arrival_time','airlines','price','durations','stopovers','layovers',
              'ratings']
    dic = {}
    for col,val in zip(columns,joined_list):
        dic[col] = val
        with open(f'data/{col}.txt','w') as f:
            for v in val:
                f.write(f'{v}\n')
    df = pd.DataFrame.from_dict(dic)
    
@click.command()
@click.argument('url')
@click.argument('dep_cou')
@click.argument('arr_cou')

def cli(url,dep_cou,arr_cou):
    get_url(url)
    flight(flight_tab)
    ticket_chooser(return_ticket)
    select_country(country_list,dep_cou,arr_cou)
    dep_date('10','5','2020')
    return_date('10','9','2020')
    search(search_tab)
    time.sleep(15)
    compile_data()
    #df.to_excel('flights.xlsx')

# In[47]:
if __name__ == '__main__':
    driver = selenium.webdriver.Chrome(executable_path="/Users/akinwande.komolafe/Downloads/chromedriver")
    cli()
 




