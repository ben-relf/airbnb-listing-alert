from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib

# config settings
driver_location = "C:\\temp\\chromedriver\\chromedriver.exe"
url = "https://www.airbnb.com.au/s/..."
results = "airbnb.csv"

# email config
email_from = 'from@gmail.com'  
email_to  = 'to@gmail.com'
email_user = 'from@gmail.com'  
email_password = ''

# list container
list_tag = "div"
list_attribute_name = "itemprop"
list_attribute_value = "itemList"
# list item
item_tag = "div"
item_attribute_name = "itemprop"
item_attribute_value = "itemListElement"
# name of the property
name_tag = "div"
name_attribute_name = "class"
name_attribute_value = "_bzh5lkq"

def notify(name, link):

    print("preparing email")
    subject = "Airbnb ALERT - {0}".format(name)
    body = "Name: {0} | Link: {1}".format(name, link).encode('utf-8')  
    message = "Subject: {0}\n\n{1}".format(subject, body)

    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)  
    server.sendmail(email_from, email_to, message)
    print("email sent")
    server.quit()

def check_site(driver):

    # create results file with header if it does not exist
    with open(results, "a") as f:
        if f.tell() == 0:
            f.write("Name|Link\n")
    
    # open driver
    driver.get(url)

    # give all the ajax content a chance to load
    time.sleep(10)

    # load contents of page into beautiful soup for parsing. 
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # find the item list
    item_list = soup.find(list_tag, attrs={list_attribute_name: list_attribute_value})
    if item_list is not None:

        # load existing results into pandas dataframe
        df = pd.read_csv(results, sep="|")

        # for each item in list
        for item in item_list.findAll(item_tag, attrs={item_attribute_name: item_attribute_value}):
            
            # get the name value for lookup
            name = item.find(name_tag, attrs={name_attribute_name: name_attribute_value}).text.strip()

            # check name against existing values in dataframe
            if not (df["Name"] == name).any():
                print("new listing - {0} found!".format(name))

                # get the link of the item
                link = "https://www.airbnb.com.au" + item.find("a", href=True)["href"]

                # save item to new data frame
                df_item = pd.DataFrame({"Name": [name], "Link": [link]})

                # append data frame to existing csv
                df_item.to_csv(results, mode="a", index=False, encoding="utf-8", sep="|", header=False)

                # notify of new entry
                notify(name, link)

            else:
                print("old listing")
                
def main():
    try:
        print("open web driver")
        driver = webdriver.Chrome(driver_location)
        check_site(driver)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        print("all finished")

if __name__ == "__main__":
    main()