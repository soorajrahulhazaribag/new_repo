import requests
from bs4 import BeautifulSoup
product_name = input("Enter Product Name to Search in Flipkart: ")
product_name = product_name.replace(" ", "+")
data = requests.get("http://www.flipkart.com/search?q="+str(product_name))
soup = BeautifulSoup(data.text, "lxml")
title_list = soup.findAll("div", {"class": "_3liAhj"}, True, None, None)
print("###############Products List####################")
for title in title_list:

    #product_title = title.find("a", {"class": "_2cLu-l"}, True, None).text
    #product_price = title.find("div", {"class": "_1vC4OE"}, True, None).text
    #print(str(product_title) + "  ===  " + str(product_price))

    product_title = title.find("a", {"class": "_2cLu-l"}, True, None).text
    product_price = title.find("div", {"class": "_1vC4OE"}, True, None).text
    print(str(product_title) + "  ===  " + str(product_price))
print("###############################################")