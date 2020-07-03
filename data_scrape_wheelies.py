#!/Users/sjamal/.conda/envs/data_scrape/bin/ python3

from bs4 import BeautifulSoup
import requests
import re
import sys
import os
from datetime import date
import smtplib

#To enable gmail to be accessed from third party app
# https://www.google.com/settings/security/lesssecureapps


#TO DO
# Create function for code snippet used in section 2 and 3 to fetch all bikes listed (optional)
# Output information to files so that notifications will only be sent whenever new changes are detected

#Meta-data used for determining data scraping logic
##See text file all_a_tag_out.txt for detailed description on iterator elements

url="https://www.wheelies.co.uk/shop/2021-bikes?psize=15"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
result_dict = {}
base_url="https://www.wheelies.co.uk"
results_dir = "/Users/sjamal/Documents/Work/9.Git_scripts/Data_Scrape/cron_results"

# Reads in tsv of specified bikes interested in querying and stores as dictionary
#=================================================================================
def tsv2dict(tsv):
    header = True
    bike_info_dict = {}
    
    with open(tsv, "r") as tsv_IN:
        for line in tsv_IN:
            #value_list = []
            nested_info_dict = {}
            line = line.strip()
            match = re.split("\t", line)
            
            if(match):
            
                if(header):
                    header_list = match
                    header = False
                    continue
                
                for i in range(0, len(match)):
                    if(header_list[i] not in nested_info_dict):
                        nested_info_dict[header_list[i]] = match[i]
                        
                
                bike_info_dict[match[0]] = nested_info_dict
                #value_list.append({ header_list[i]: match[i] })



    return(bike_info_dict)

def send_notification(boolean_dict, possible_match_message):
    
    new_2021_key = "new_2021_bikes"
    new_cannondale_key = "new_cannondale_bikes_bol"
    new_specialized_key = "new_specialized_bikes_bol"
    cannondale = False
    specialized = False
    status = 0
    
    ##Email 1
    #========
    if(boolean_dict[new_2021_key] and boolean_dict[new_cannondale_key]):
        cannondale = True
        category = "cannondale".upper()
        status = 1

        sender = "Sabri Jamal <mypydevapp@gmail.com>"
        receiver = ["Sabri Jamal <mypydevapp@gmail.com>", "Sabri Jamal <s.jamal@live.se>", "Carmen Alvarez Campo <carmen_alvarez_campo@hotmail.com>"]
        port = 587

        message = f"""\
Subject: *!{category} BIKE NOTIFICATION*!
To: {receiver}
From: {sender}

New 2021 CANNONDALE bike on Wheelies.

***POSSIBLE MATCHES, NOT BRAND SPECIFIC
{possible_match_message}"""

        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.ehlo()
            server.starttls()
            server.login("mypydevapp@gmail.com", "appdevpymy")
            server.sendmail(sender, receiver, message)
            server.quit()

    ##Email 2
    #========
    if(boolean_dict[new_2021_key] and boolean_dict[new_specialized_key]):
        specialized = True
        category = "specialized".upper()
        status = 2
        
        sender = "Sabri Jamal <mypydevapp@gmail.com>"
        receiver = ["Sabri Jamal <mypydevapp@gmail.com>", "Sabri Jamal <s.jamal@live.se>", "Carmen Alvarez Campo <carmen_alvarez_campo@hotmail.com>"]
        port = 587

        message = f"""\
Subject: *!{category} BIKE NOTIFICATION*!
To: {receiver}
From: {sender}

New 2021 SPECIALIZED bike on Wheelies.

***POSSIBLE MATCHES, NOT BRAND SPECIFIC
{possible_match_message}"""

        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.ehlo()
            server.starttls()
            server.login("mypydevapp@gmail.com", "appdevpymy")
            server.sendmail(sender, receiver, message)
            server.quit()

    ##Email 3
    #========
    if(boolean_dict[new_2021_key] and not cannondale and not specialized):
        category = "2021"
        status = 3
        
        sender = "Sabri Jamal <mypydevapp@gmail.com>"
        receiver = ["Sabri Jamal <mypydevapp@gmail.com>", "Sabri Jamal <s.jamal@live.se>", "Carmen Alvarez Campo <carmen_alvarez_campo@hotmail.com>"]
        port = 587

        message = f"""\
Subject: *!{category} BIKE NOTIFICATION*!
To: {receiver}
From: {sender}

New 2021 bikes on Wheelies.

***POSSIBLE MATCHES, NOT BRAND SPECIFIC
{possible_match_message}"""

        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.ehlo()
            server.starttls()
            server.login("mypydevapp@gmail.com", "appdevpymy")
            server.sendmail(sender, receiver, message)
            server.quit()

    return(status)

# Section 1 to fetch information on all 2021 bikes listed and store as json or yml or nested dict
#=================================================================================================

#Instantiate variables
scrapped_bike_info_dict = {}

for tag in soup.find_all('a'):
    
    ##Scrape site for total number of 2021 bikes
    total_bike_match_tag = re.search('data-ga-label="2021_Bikes"', str(tag))
    
    if(total_bike_match_tag):
        span_tag_list = tag.find_all("span")
        
        for item in span_tag_list:
            total_bike_match_int = re.search('>\((\d+)\)<', str(item))
            
            if(total_bike_match_int):
                if("total_2021_bikes" in result_dict):
                    print("WARNING! There matches for scraping total bikes exceeded 1, non-unique match review!")
                else:
                    result_dict['total_2021_bikes'] = total_bike_match_int.group(1)
                    
    ##Scrape site for total number of Cannondale bikes
    total_cannondale_match_tag = re.search('data-ga-label="Cannondale_Bikes"', str(tag))
    
    if(total_cannondale_match_tag):
        span_tag_list = tag.find_all("span")
        
        for item in span_tag_list:
            total_cannondale_match_int = re.search('>\((\d+)\)<', str(item))
            
            if(total_cannondale_match_int):
                if("total_cannondale_2021_bikes" in result_dict):
                    print("WARNING! The matches for scraping total cannondale bikes exceeded 1, non-unique match review!")
                else:
                    result_dict['total_cannondale_2021_bikes'] = total_cannondale_match_int.group(1)
    
    
    ##Scrape site for total number of Specialized bikes
    total_Specialized_match_tag = re.search('data-ga-label="Specialized_Bikes"', str(tag))

    if(total_Specialized_match_tag):
        span_tag_list = tag.find_all("span")

        for item in span_tag_list:
            total_Specialized_match_int = re.search('>\((\d+)\)<', str(item))

            if(total_Specialized_match_int):
                if("total_Specialized_2021_bikes" in result_dict):
                        print("WARNING! The matches for scraping total Specialized bikes exceeded 1, non-unique match review!")
                else:
                        result_dict['total_Specialized_2021_bikes'] = total_Specialized_match_int.group(1)
                        
    # Section 2 scrape and store information on each bike for page 1
    #=====================================================================
    ##Scrape site for all bikes on offer (store in dict)
    #Unique string in tag for bikes on offer data-ga-label="/shop (no duplicates)
    #Loop each page; id for page 2 is shop/2021-bikes?psize=15&page=2 
    #   (full name: https://www.wheelies.co.uk/shop/2021-bikes?psize=15&page=2)
    #   Either loop all a hrefs as in section 3 or fetch from section 1 loop directly

    ##Scrape site for brand, model and value for bikes on page 1
    bikes_for_sale_match_tag = re.search('data-ga-label="/shop', str(tag))
    
    if(bikes_for_sale_match_tag):
        brand_match = None
        model_match = None
        value_match = None
        
        for item in tag.find_all("span"):
            
            if(not brand_match):
                brand_match = re.search('"brand">(.+)<', str(item))
            
            if(not model_match):
                model_match = re.search('model ellipsis.+>(.+)<', str(item))
                
            if(not value_match):
                value_match = re.search('value">(.+)<', str(item))
            
            if(brand_match and model_match and value_match):
                nested_info_dict = {}
                nested_info_dict[model_match.group(1)] = value_match.group(1)

                if(brand_match.group(1) not in scrapped_bike_info_dict):
                    scrapped_bike_info_dict[brand_match.group(1)] = nested_info_dict
                else:
                    nested_info_dict_tmp = scrapped_bike_info_dict[brand_match.group(1)]
                    nested_info_dict_tmp[model_match.group(1)] = value_match.group(1)
                    scrapped_bike_info_dict[brand_match.group(1)] = nested_info_dict_tmp
                    
                brand_match = None
                model_match = None
                value_match = None
                    
##Section 3 - Scrape bike info for all other pages other than page 1
#===================================================================

##Fetch all pages where bikes are listed and store to dict
bike_pages_dict = {}
page_count = 2
for tag in soup.find_all("a"):
    link = tag.get("href")
    match = re.search('/shop/2021-bikes\?psize=15&page=\d+', str(link))
    if(match):
        if(match.group() not in bike_pages_dict):
            bike_pages_dict[match.group()] = "page {page_count}".format(page_count=page_count)
            page_count += 1
            
            
##Loop pages dict (bike_pages_dict) and more or less copy paste script from section 2 (Create function?)

#Print header for action to stdout
print("\n***SCRAPING PAGES") 

for page_url, page_count_string in bike_pages_dict.items():
    print("Scraping {page_count_string} for brand, model and bike value".format(page_count_string=page_count_string))
    
    r = requests.get("{base}/{page}".format(base=base_url,page=page_url))
    soup = BeautifulSoup(r.content, 'html.parser')
    
    for tag in soup.find_all("a"):
        
       ##Scrape site for brand, model and value for bikes on page 1
        bikes_for_sale_match_tag = re.search('data-ga-label="/shop', str(tag))

        if(bikes_for_sale_match_tag):
            brand_match = None
            model_match = None
            value_match = None

            for item in tag.find_all("span"):

                if(not brand_match):
                    brand_match = re.search('"brand">(.+)<', str(item))

                if(not model_match):
                    model_match = re.search('model ellipsis.+>(.+)<', str(item))

                if(not value_match):
                    value_match = re.search('value">(.+)<', str(item))

                if(brand_match and model_match and value_match):
                    nested_info_dict = {}
                    nested_info_dict[model_match.group(1)] = value_match.group(1)

                    if(brand_match.group(1) not in scrapped_bike_info_dict):
                        scrapped_bike_info_dict[brand_match.group(1)] = nested_info_dict
                    else:
                        nested_info_dict_tmp = scrapped_bike_info_dict[brand_match.group(1)]
                        nested_info_dict_tmp[model_match.group(1)] = value_match.group(1)
                        scrapped_bike_info_dict[brand_match.group(1)] = nested_info_dict_tmp

                    brand_match = None
                    model_match = None
                    value_match = None
        

# Section 4 search json/yml/nested dict for bikes of interest 
#===============================================================
bikes_to_search_dict = tsv2dict("/Users/sjamal/Documents/Non-work_related/Bike/New_bike_review.txt")
bike_match_dict = {}

#Print header for action to stdout
print("\n***VERBOSE COMPARISON OF KEYWORD VS SCRAPED BIKES") 

for my_bike_model, my_bike_info_dict in bikes_to_search_dict.items():
    if(my_bike_info_dict['Brand'] in scrapped_bike_info_dict):
        bike_info_by_brand = scrapped_bike_info_dict[my_bike_info_dict['Brand']]
        scrapped_models_list = list(bike_info_by_brand.keys())

        #CONTINUE HERE <PART WHERE SEARCH CAN BE MADE MORE SOPHISTICATED!> OR REMOVE COMPONENT NAME FROM TSV
        for scrapped_model in scrapped_models_list:
            match = re.search(my_bike_model.lower(), scrapped_model.lower())

            print("COMPARING {my_bike_model}\t VS \t{scrapped_model}".format(my_bike_model=my_bike_model, scrapped_model=scrapped_model ))

            if(match):
                if(scrapped_model not in bike_match_dict):
                    bike_match_dict[scrapped_model] = [my_bike_model, my_bike_info_dict['Brand']]
                else:
                    print("Error non unique bike models on Wheelies website")

#Report possible bike matches

#Print header for action to stdout
print("\n***POSSIBLE MATCHES DETECTED") 

possible_matches_message = ""
for scrapped_model, listed_model_list in bike_match_dict.items():
    print("Possible {my_model} match found comparing {my_model}\t<=>\t{scrapped_model}".format(scrapped_model=scrapped_model, my_model=listed_model_list[0], my_brand=listed_model_list[1]))
    
    possible_matches_message = "{possible_matches_message}\nPossible match, {my_model}\t<=>\t{scrapped_model}".format(possible_matches_message=possible_matches_message, scrapped_model=scrapped_model.upper(), my_model=listed_model_list[0].upper(), my_brand=listed_model_list[1].upper())

# Section 5 write data to file
#=============================
    
def result_dict2file(result_dict):
    extension = "." + str(date.today())
    for key,val in result_dict.items():
        with open(os.path.join(results_dir, key + extension), "w") as OUT:
            OUT.write(val)
            
def bike_match_dict2file(bike_match_dict):
    extension = "." + str(date.today())
    with open(os.path.join(results_dir, "matching_bike" + extension), "w") as OUT:
        for key, val_list in bike_match_dict.items():
            OUT.write('Found {bike_found}\n\tMy listed bike - {search_pattern}\n\tBrand - {brand}\n\n'.format(bike_found=key.upper(), search_pattern=val_list[0].upper(), brand=val_list[1].upper()))

# Section 6 Compare todays data from yesterday
#=============================================
previous_day_file = os.path.join(results_dir,"0.files_previous_day.txt")
#file_name_matching_bike = os.path.join(results_dir, "matching_bike")
file_name_tot2021 = os.path.join(results_dir, "total_2021_bikes")
file_name_tot_cannondale = os.path.join(results_dir, "total_cannondale_2021_bikes")
file_name_tot_specialized = os.path.join(results_dir, "total_Specialized_2021_bikes")
new_2021_bikes_bol = False
new_cannondale_bikes_bol = False
new_specialized_bikes_bol = False
prev_day_bike_values_dict = {}

if(os.path.exists(previous_day_file)):
    with open(previous_day_file, "r") as prev_day_IN:
        for file in prev_day_IN:
            file = file.strip()
            file_base_name = file.split("/")[-1].split(".")[0]
            
            today_total_2021_bikes = result_dict['total_2021_bikes']
            today_cannondale_bikes = result_dict['total_cannondale_2021_bikes']
            today_specialized_bikes = result_dict['total_Specialized_2021_bikes']
            
            #Store bikes numbers prev day and compare to today 
            with open(file, "r") as IN:
                for line in IN:
                    line = line.strip()
                    prev_day_bike_values_dict[file_base_name] = line
                    
    if(int(today_total_2021_bikes) > int(prev_day_bike_values_dict['total_2021_bikes'])):
        new_2021_bikes_bol = True

    if(int(today_cannondale_bikes) > int(prev_day_bike_values_dict['total_cannondale_2021_bikes'])):
        new_cannondale_bikes_bol = True

    if(int(today_specialized_bikes) > int(prev_day_bike_values_dict['total_Specialized_2021_bikes'])):
        new_specialized_bikes_bol = True
        
    email_bol_dict = {
        "new_2021_bikes": new_2021_bikes_bol,
        "new_cannondale_bikes_bol": new_cannondale_bikes_bol,
        "new_specialized_bikes_bol": new_specialized_bikes_bol
    }
        

# Section 7 overwrite file names stored in previous day file to be compared with "tomorrow"
#==========================================================================================
with open(previous_day_file, "w") as OUT:
    OUT.write("{file_name_tot2021}.{date}\n".format(file_name_tot2021=file_name_tot2021, date=str(date.today())))
    OUT.write("{file_name_tot_cannondale}.{date}\n".format(file_name_tot_cannondale=file_name_tot_cannondale, date=str(date.today())))
    OUT.write("{file_name_tot_specialized}.{date}\n".format(file_name_tot_specialized=file_name_tot_specialized, date=str(date.today())))

##Output found data to file
result_dict2file(result_dict)
bike_match_dict2file(bike_match_dict)

#Section 8 - Send notification email if new bikes listed
#Print header for action to stdout
print("\n***DEBUGER") 

print(email_bol_dict)
status = send_notification(email_bol_dict, possible_matches_message)
print("Moved into condition {status}".format(status=status))
