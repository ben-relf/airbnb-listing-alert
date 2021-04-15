from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import configparser
import smtplib
import time
import os

CONFIG_FILE_NAME = 'user.cfg'
NO_OF_SITES = 2

# Init config
config = configparser.ConfigParser()
if not os.path.exists(CONFIG_FILE_NAME):
    print('No configuration file (user.cfg) found! See README.')
    exit()
config.read(CONFIG_FILE_NAME)

# email config
email_from = config.get('user_config', 'email_from')
email_to  = config.get('user_config', 'email_to')
email_user = config.get('user_config', 'email_user')
email_password = config.get('user_config', 'email_password')

def notify_site(site, name, price, link):

    subject = '{0} ALERT - {1} {2}'.format(site, name, price)
    body = "Name: {0} | Price: {2} | Link: {1}".format(name, link, price).encode('utf-8')  
    message = "Subject: {0}\n\n{1}".format(subject, body)
    send_email(subject, body, message)

def notify_error(err):

    subject = 'Listing Alert ERROR'
    body = '{0}'.format(err)  
    message = 'Subject: {0}\n\n{1}'.format(subject, body)
    send_email(subject, body, message)

def send_email(subject, body, message):

    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)  
    server.sendmail(email_from, email_to, message)
    print("email sent")
    server.quit()

def check_site(driver):

    for site in range(NO_OF_SITES):
        site_config = 'site_{0}_config'.format(site)
        url = config.get(site_config, 'search_url')
        results = 'results_{0}.csv'.format(config.get(site_config, 'site'))
        # property list
        list_tag = config.get(site_config, 'list_tag')
        list_attribute_name = config.get(site_config, 'list_attribute_name')
        list_attribute_value = config.get(site_config, 'list_attribute_value')
        # property item
        item_tag = config.get(site_config, 'item_tag')
        item_attribute_name = config.get(site_config, 'item_attribute_name')
        item_attribute_value = config.get(site_config, 'item_attribute_value')
        # name of the property
        name_tag = config.get(site_config, 'name_tag')
        name_attribute_name = config.get(site_config, 'name_attribute_name')
        name_attribute_value = config.get(site_config, 'name_attribute_value')
        # price of the property
        price_tag = config.get(site_config, 'price_tag')
        price_attribute_name = config.get(site_config, 'price_attribute_name')
        price_attribute_value = config.get(site_config, 'price_attribute_value')

        # create results file with header if it does not exist
        with open(results, 'a') as f:
            if f.tell() == 0:
                #f.write('Name|Description|Price|Link\n')
                f.write('Name|Price|Link\n')
    
        driver.get(url) # open driver
        time.sleep(10) # give all the ajax content a chance to load
        soup = BeautifulSoup(driver.page_source, 'html.parser') # load contents of page into beautiful soup for parsing. 
        item_list = soup.find(list_tag, attrs={list_attribute_name: list_attribute_value}) # find the item list
        if item_list is not None:
            df = pd.read_csv(results, sep="|") # load existing results into pandas dataframe
            # for each item in list
            for item in item_list.findAll(item_tag, attrs={item_attribute_name: item_attribute_value}):  
                # get the name value for lookup
                name = item.find(name_tag, attrs={name_attribute_name: name_attribute_value}).text.strip()

                # check name against existing values in dataframe
                if not (df["Name"] == name).any():
                    print("new listing - {0} found!".format(name))

                    price_html = item.find(price_tag, attrs={price_attribute_name: price_attribute_value})
                    if price_html is not None:
                        price = price_html.text.strip()
                    else:
                        price = "price not found"

                    link = config.get(site_config, 'base_url') + item.find("a", href=True)["href"] # get the link of the item
                    
                    df_item = pd.DataFrame({"Name": [name], "Price": [price], "Link": [link]}) # save item to new data frame
                    df_item.to_csv(results, mode="a", index=False, encoding="utf-8", sep="|", header=False) # append data frame to existing csv
                    
                    #notify of new entry
                    notify_site(config.get(site_config, 'site'), name, price, link)

                else:
                    print("old listing")
                
def main():
    try:
        driver = webdriver.Chrome(config.get('user_config', 'driver_location'))
        check_site(driver)
    except Exception as e:
        print(e)

    finally:
        driver.quit()
        print("all finished")

if __name__ == "__main__":
    main()