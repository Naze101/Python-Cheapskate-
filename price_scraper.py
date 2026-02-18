#This will scrape ram product prices from websites
# # import libraries (Selenium for web scraping, matplotlib for graph, pandas for creating a 2d data table, time for getting time and using intervals )

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# Selenium used for webscraping
import time # used with selenium
from datetime import datetime # using for time stamps

import matplotlib # for graphing
import matplotlib.pyplot as plt # for graphing

import pandas as pd # Used for dataframe/2d dimensions
import json # used for converting data in python into json - a formatter
import os # used for accessing files

#connecting our json file with our python file
data_holder_newegg = "newegg_organizer.json" 
data_holder_ebay = "ebay_organizer.json"
# Get prices of RAM from Amazon, Newegg, Best Buy, Ebay, Ali Baba (??)
# use function(s) for this

#function to get time and correlate with price
def record_price_newegg(): # record price and correlate with time
    price = search_newegg()
    if price: #if we actually get the price
        history = load_price_history_newegg() # history = dictionary
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history["newegg"].append({
            "price": price,
            "timestamp": timestamp
        })
        save_price_newegg(history)
        print(f"Recorded price: ${price} at {timestamp}")
        return price
    else:
        print("failed to scrape price")
        return None

def record_price_ebay(): # record price and correlate with time
    price = search_ebay()
    if price: #if we actually get the price
        history = load_price_history_ebay()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history["ebay"].append({
            "price": price,
            "timestamp": timestamp
        })
        save_price_ebay(history)
        print(f"Recorded price: ${price} at {timestamp}")
        return price
    else:
        print("failed to scrape price")
        return None

# Function to load price into json holder
def save_price_newegg(data):
    with open(data_holder_newegg, 'w') as f:
        json.dump(data, f, indent=2)

def save_price_ebay(data):
    with open(data_holder_ebay, 'w') as f:
        json.dump(data, f, indent=2)
    

def load_price_history_newegg(): #This gets data from json file to use when making graph
    # get data from json
    if os.path.exists(data_holder_newegg):  
        with open (data_holder_newegg, 'r') as f:
            return json.load(f)
    return {"newegg": []}

def load_price_history_ebay(): #This gets data from json file to use when making graph
    # get data from json
    if os.path.exists(data_holder_ebay):  
        with open (data_holder_ebay, 'r') as f:
            return json.load(f)
    return {"ebay": []}

#Function to put data into matplotlib graph
def search_newegg():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(
        service=Service(options=options)
    )

    driver.get("https://www.newegg.ca/corsair-vengeance-lpx-32gb-ddr4-3200-cas-latency-cl16-desktop-memory-black/p/N82E16820236541")
    time.sleep(3) # waiting for page load
    price = driver.find_element(By.CSS_SELECTOR, "div.price-current")
    price_element = price.text.replace("$", " ")
    print(price_element)
    return float(price_element)

def search_ebay():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--incognito")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(
        service=Service(options=options)
    )

    driver.get("https://www.ebay.ca/itm/236641579200?_skw=ram+vengeance&epid=2334409862&itmmeta=01KHS18X269Z08N6PNSMEBRDKD&hash=item3718eff0c0:g:W4oAAeSwXgJpiN-v&itmprp=enc%3AAQALAAAA8GfYFPkwiKCW4ZNSs2u11xCKSUrE2r3Ue4TXDors3UhcfEjv49wJ5UAzNy%2Bt6UvDkdXKK4Uu90xW1DlWNpKaZaHji23QY6R4NQDiDkCDtecD2d4ZK9yBk%2B3xLO8IIxpQRxAFfqWHauPxL%2Fw2aIu9jTfv2PsO0lQ3gFDu0b%2Fy53DW9BEn0hASXkK3xq6c242oq5MYNydaXlnqrNjP2p%2F9MXW2Kq2fkX7M0rnPSf7AgYTex2bFnGOSrVViMz6Dqs7BUNezioOofcziBZ9LYw0MBuG8XBYoyl24S%2FnWAOfE6HBwuUWTzrncfZ5LraKXfjiimA%3D%3D%7Ctkp%3ABFBMpNGjoY5n")
    time.sleep(3) # waiting for page load
    price = driver.find_element(By.CLASS_NAME, "x-price-primary")
    price_element = price.text.replace("$", " ").replace("C", " ")
    print(price_element)
    return float(price_element)


def plot_prices():
    # time to plot prices on graph using matplotlib!
   
    #pandas data table creation
    history1 = load_price_history_newegg() # function returns python dictionary of stuff in json file
    history2 = load_price_history_ebay()

    if not history1["newegg"]:
        print("No newegg price history available")
        return
    if not history2["ebay"]:
        print("No ebay price history available")
        return
    
    # df1 = NEWEGG, df2 = EBAY
    df1 = pd.DataFrame(history1["newegg"])
    df1["timestamp"] = pd.to_datetime(df1["timestamp"])
    df1 = df1.sort_values("timestamp")

    df2 = pd.DataFrame(history2["ebay"])
    df2["timestamp"] = pd.to_datetime(df2["timestamp"])
    df2 = df2.sort_values("timestamp")


    #matplotlib graph creation
    plt.figure(figsize = (12,6))
    plt.plot(df1["timestamp"], df1["price"], label = 'Newegg', marker = 'o', linestyle='-', linewidth=2)
    plt.plot(df2["timestamp"], df2["price"], label = 'Ebay', marker = 'o', linestyle='-', linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Price ($)")
    plt.title("Ram Prices over time")
    plt.xticks(rotation=45)
    plt.tight_layout() # makes figure fit in given size
    plt.savefig("price_history.png")
    plt.show()
    return df1, df2


#looping so code runs at regular intervals

while True:
    try:
        record_price_ebay()
        record_price_newegg()
        plot_prices()
    except Exception as e:
        print("The code has failed")
    time.sleep(30) # sleep 60 seconds and update

record_price_ebay()
record_price_newegg()
plot_prices()