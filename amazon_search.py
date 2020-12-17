# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import random
from bs4 import BeautifulSoup
from nordvpn_switcher import rotate_VPN,terminate_VPN

from selenium import webdriver
from time import sleep

settings = {'opsys': 'Windows', 'command': ['nordvpn', '-c', '-g'], 'settings': ['india'], 'cwd_path': 'C:/Program Files/NordVPN'}


url = "http://www.amazon.in/"
query = url+"s?k="

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"]


def wordsearch(string,words):
    count = 0
    total = 0
    for word in words:
        total += 1
        if(word in string):
            count += 1
    return round((count/total)*100,2)
     

def amzsearch(url,product,header,page):
    
    print("Page No: "+page.__str__())
    print("Opening connection...")
    print("-------------------")
    
    response = requests.get(url, headers={'User-Agent':header})
    links = {}

    if(response.status_code == 200):
        print("Connection is open now.")
        print("-------------------")
        soup = BeautifulSoup(response.text,"html.parser")
        listings = soup.findAll('a',class_='a-link-normal a-text-normal')
        for listing in listings:
            link = "http://www.amazon.in"+listing['href']
            if(link not in links) and ('redirect' not in link):
                links[link] = listing.text
                
    
        for link in links:
            print(links[link])
            matching_probab = wordsearch(links[link].lower(), product)
            print(matching_probab.__str__()+"%")
            if(matching_probab>89.9):
                print("Found the product.")
                print("Opening product details page...")
                print("-------------------")
                try:
                    driver = webdriver.Chrome(executable_path="chromedriver.exe")
                    print(link)
                    driver.get(link)
                    driver.implicitly_wait(5)
                    driver.find_element_by_name('submit.add-to-cart').click()
                    print("Product added to cart!")
                    print("-------------------")
                    
    
                    print("Wait for 10 secs")
                    print("-------------------")
                    timer = 0
                    while timer < 10:
                        timer = timer+1
                        sleep(1)
                    driver.close()
                except Exception as ex:
                    print(ex)
                return
            print("------------------")
            
        next_page = soup.find('li',class_='a-last')
        try:
            next_page_link = "https://amazon.in"+next_page.find('a')['href']
            print("Next Page")
            print(next_page_link)
            amzsearch(next_page_link, product, header, page+1)
        except:
            print("That was the last page.")
            print("------------------")
            
    else:
        print("Failed to open the connection.")
        print("-------------------")
            
def repeat_script(url,product):
    
    print("Rotatting VPN")
    try:
        rotate_VPN(settings)
    except:
        print("Rotation Failed")
    finally:
        print("----------------")
    
    header = random.choice(user_agents)
    print("User Agent")
    print(header)
    print("----------------")
    
    amzsearch(url, product, header, 1) 
    print("Disconnecting VPN")
    try:
        terminate_VPN(settings) 
    except:
        print("Disconnection Failed")
    finally:
        print("----------------")
        sleep(5)
        repeat_script(url, product)


print("----------------")
print("AMAZON.IN AUTO SEARCHING SCRIPT")
print("----------------")

product = input("Enter product name: ")
keywords = input("Enter search query: ")
product = product.lower().split(" ")
keywords = keywords.strip().replace(" ", "+")

print("\nScript started.\nIt will continue to run untill product is not found using given query or untill all pages are visited.")
print("-------------------")

repeat_script(query+keywords,product)
