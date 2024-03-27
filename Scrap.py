import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


## Uncomment one line per run: As all these reports are in different urls/sections:

# COMMENT: this is for all reports
# url = 'http://www.ipaidabribe.com/reports/all#gsc.tab=0'

# COMMENT: this url is for bribe fighter reports
# url = "http://www.ipaidabribe.com/reports/bribe-fighter?page=#gsc.tab=0"
# MANUALLY FOUND OUT NUMBER OF PAGES AVAILABLE IN THIS SECTION : #3551

# COMMENT: this url is for I met an honest officer report
# url = "http://www.ipaidabribe.com/reports/honest-officer?page=#gsc.tab=0"
# MANUALLY FOUND OUT NUMBER OF PAGES AVAILABLE IN THIS SECTION : #1080

# COMMENT: This report was selected randomly so I can see if how to get the all the details needed in the story:
# url = "http://www.ipaidabribe.com/reports/paid/bribe-for-change-in-name-in-noida-authority#gsc.tab=0"

reqs = requests.get(url) #This will get the data from the webpage
soup = BeautifulSoup(reqs.text, 'html.parser') #Website data is converted to readable format using BeautifulSoup library.
## urls = [url]

urls = []

# COMMENT: this will scrape all the links included in a page of the website
for link in soup.find_all('a'):
    (urls.append(str(link.get('href'))))

data = []

# This Section is used to filter out links which contain stories:
filtered_urls = []
filter = "http://www.ipaidabribe.com/reports/honest-officer/"
# filter = "http://www.ipaidabribe.com/reports/bribe-fighter/"
len1 = len(filter)
print("First page done.")

for link in urls:
    # #print(link)
    # #print(link, len(link))
    if len(str(link)) > 40 :
        if link[0:len1] == filter and link not in filtered_urls:
          # print(f"ADDING in filtered : {link}")
          filtered_urls.append(link)

#print(len(urls))
# urls

print("For getting data from other pages:")
for i in range(10, 1081, 10):
    url = f"http://www.ipaidabribe.com/reports/honest-officer?page={i}#gsc.tab=0"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    print(f"GOING to {i}th page out of {1080}")
    # main_urls.clear()
    urls.clear()
    # urls = main_urls
    for link in soup.find_all('a'):
        (urls.append(str(link.get('href'))))
        # #print(len(urls),i)
    for link in urls:
        if len(str(link)) > 40:
            if link[0:len1] == filter and link not in filtered_urls:
              # #print(f"ADDING in filtered : {link}")
              filtered_urls.append(link)
    # #print(len(filtered_urls))
    print(len(filtered_urls))


# This section will now go to every link separately and scrape the needed data.
i = 0
for url in filtered_urls:
    print(i,len(filtered_urls))
    i = i + 1; #To see live progress of how much data has been scraped.
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        names = soup.find('div', class_='report-listing details')  # .find('a').text.strip()
        # names = soup.find_all('p',class_ = 'body-copy-lg')
        # names = soup.find_all('p',class_ = 'body-copy-lg').text.strip()
        report_number = names.find('span', class_="unique-reference").get_text()
        # print(report_number)
        report_posting_date = names.find('span', class_="date").get_text()
        # print(report_posting_date)
        location = names.find('a', class_="location").text.replace(",","#").strip().split("#")
        city = location[0].replace("\r\n                      ","")
        try:
            state = location[-1]
        except:
            state = "$$"
        # print(city,state,sep=", ")
        office_type = names.find('ul', class_="department clearfix").find('li', class_='name').text.strip()
        # print(office_type)
        work_kind = names.find('ul', class_="department clearfix").find('li', class_='transaction').text.strip()
        # print(work_kind)
        try:
            paid_amount = names.find('ul', class_="department clearfix").find('li', class_='paid-amount').text.strip()
        except:
            paid_amount = "Paid INR 0"
        # print(paid_amount)
        label = names.find('a').text.strip()
        # print(label)
        full_story = names.find('p', class_="body-copy-lg").text.strip()
        # print(full_story)

        #The below section of code will add new data to the previous data to form a List
        data.append({"Report Number": report_number,
                     "Report Posting Date": report_posting_date,
                     "City": city,
                     "State": state,
                     "Office Type": office_type,
                     "Kind of work": work_kind,
                     "Bribe Amount Paid": paid_amount,
                     "Link":url,
                     "Label": label,
                     "Full Story": full_story,
                     "IPaidABribe":0,
                     "IDidNotPayABribe":0,
                     "IMetAnHonestOfficer":1
                     })
    except:
        pass

# print(data)

# print(data)

#This section will convert List to excel file and save the file with the name mentioned below:
df = pd.DataFrame(data)
df.to_excel('IMetAnHonestOfficer.xlsx',index=False)
print("Finished making EXcel")