import requests
from bs4 import BeautifulSoup
product_name = input("Enter Product Name to Search in Flipkart: ")
product_name = product_name.replace(" ", "+")
data = requests.get("http://www.flipkart.com/search?q="+str(product_name))
soup = BeautifulSoup(data.text, "lxml")
#_3liAhj == mouse, keyboard_element , col _2-gKeQ == laptop, mobile_element ,
title_list = soup.findAll(True, {"class": ["_3liAhj", "col _2-gKeQ"]}, True, None, None)
print("###############Products List####################")
for title in title_list:

    product_title = title.find(True, {"class": ["_2cLu-l", "_3wU53n"]}, True, None).text
    product_price = title.find("div", {"class": ["_1vC4OE", "_1vC4OE _2rQ-NK"]}, True, None).text
    print(str(product_title) + "  ===  " + str(product_price))
    mylink = title.find('a')
    texty = mylink.attrs['href']
    print(texty)
print("###############################################")


item_name = input("Copy And paste the link of a product of your choice :  ")
item_name = item_name.replace(" ", "+")
data = requests.get("http://www.flipkart.com"+str(item_name))
soup1 = BeautifulSoup(data.text, "lxml")

review_list = soup1.findAll("div", {"class": "col _390CkK"}, True, None, None)
print("###############Review List####################")
i=1
for review in review_list:
    print(str(i)+">")
    item_review = review.find("div", {"class": "qwjRop"}, True, None).text
    #item_rating = review.find("div", {"class": "hGSR34 _2beYZw E_uFuv"}, True, None).text
    print(str(item_review))

    with open('flipkartdata.txt', 'a') as f:
        f.write(str(i)+">  ")
        f.write(item_review)
        f.write("\n \n")

    i=i+1
print("###############################################")