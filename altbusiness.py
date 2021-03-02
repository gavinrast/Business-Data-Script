# Gavin Rast
# Business Script
# 2/3/20

import time
import csv
import os
import sys
import re
from random import randint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

# ----------------------------------------------------------------------

# Start of main program
if __name__ == '__main__':

    # Opens the csv business input file
    with open('WorkDatabaseParsetoCSV.csv') as csv_input:
        company_as_list = []
        address_as_list = []
        read_index = 0
        
        # Parses each line with ',' as the delimiter
        for current_line in csv_input:
            temp_list = current_line.split(",")
            company_as_list.append(temp_list[0])
            address_as_list.append(temp_list[1].rstrip('\n'))
            read_index += 1
        total_inputs = int(len(company_as_list))
        
    csv_input.close()

    # Opens the csv business output file
    with open('infooutput2.csv', mode='w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        options = Options()
        
        # Options to run as headless browser and with speed catches
        options.headless = False
        speedcatch = True
        
        # Sets executable path to the directory path of the webdriver.
        driver = webdriver.Chrome(executable_path=r'\chromedriver.exe',
                                  options=options)

        # Main running loop that searches until the max total inputs has been reached
        for current_business in range(0, total_inputs):
            
            # Variable check for pop-up prompts
            prompted = 0
            
            # Slows down the program if speedcatch is true
            if speedcatch:
                time.sleep(randint(1, 5))
            
            # Sets the target website
            driver.get("https://www.bbb.org/")
            driver.maximize_window()
            
            # Sends the business name
            if speedcatch:
                time.sleep(randint(5, 8))
            
            insert_business_name = company_as_list[current_business]
            business_name_inputbox = driver.find_element_by_xpath('//*[@id="findTypeaheadInput"]')
            business_name_inputbox.send_keys(insert_business_name)
            
            # Sends the target location
            if speedcatch:
                time.sleep(randint(3, 5))
            
            clear_input_bin = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div/div[2]/div/form/div[2]/div[2]/button')
            clear_input_bin.click()
            business_area_inputbox = driver.find_element_by_xpath('//*[@id="nearTypeaheadInput"]')
            business_area_inputbox.send_keys('Phoenix, AZ')
            
            # Activates search command
            if speedcatch:
                time.sleep(randint(1, 5))
            
            search_box = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div/div[2]/div/form/div[2]/button')
            search_box.click()
            
            if speedcatch:
                time.sleep(randint(1, 5))
            
            # Attempts to click popup propmt
            try:
                clickable_btn = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/div[2]/fieldset/div[1]/label[2]/div/span/span[1]/input')
                print("Prompt box")
                clickable_btn.click()
                prompted = 1
            except NoSuchElementException:
                print("No prompt box")

            # Gets the amount of business results on the page
            total_nums = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[1]/h2/strong[1]'
            
            # Attempts to set the max number of results to the number on the page
            try:
                current_total = driver.find_element_by_xpath(total_nums).text
                max_number = int(current_total)
            except NoSuchElementException:
                max_number = 0
                
            # Dislays the total number of results
            print(max_number)
            
            # Caps the page limit to 15 search results
            if max_number > 0:
                if max_number > 15:
                    max_number = 15
                    
                # Sets the target div container
                current_address_index = 4
                
                # Loops through the page to find the target business data
                for index in range(0, max_number):
                    business_address_return1 = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[%s]/div/div/div[2]/div[1]/p[2]'
                    business_address_return2 = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[%s]/div/div/div[2]/div[1]/p[3]'
                    bar1 = business_address_return1 % current_address_index
                    bar2 = business_address_return2 % current_address_index
                    
                    # Attempts to get the current business name and address (multiple attempts due to div-shifting on the page)
                    try:
                        present_address1 = driver.find_element_by_xpath(bar1)
                        found_address1 = present_address1.text
                    except NoSuchElementException:
                        found_address1 = "nothing"
                    try:
                        present_address2 = driver.find_element_by_xpath(bar1)
                        found_address2 = present_address2.text
                    except NoSuchElementException:
                        found_address2 = "nothing"
                    if found_address1 == address_as_list[current_business] or \
                            found_address1 in address_as_list[current_business] or \
                            address_as_list[current_business] in found_address1:
                        found_address = found_address1
                    else:
                        found_address = found_address2
                    print(found_address)
                    business_write = company_as_list[current_business]
                    address_write = address_as_list[current_business]

                    if found_address == address_as_list[current_business] or\
                            found_address in address_as_list[current_business] or\
                            address_as_list[current_business] in found_address:
                        print(business_write)
                        
                        # Attempts to navigate to business page to get data
                        try:
                            if prompted == 0:
                                try:
                                    clickable_btn = driver.find_element_by_xpath(
                                        '/html/body/div[2]/div[3]/div/form/div[2]/fieldset/div[1]/label[2]/div/span/span[1]/input')
                                    print("Prompt box")
                                    clickable_btn.click()
                                except NoSuchElementException:
                                    print("No prompt box")
                            click_get_bus_info = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[4]')
                            click_get_bus_info.click()
                            
                            if speedcatch:
                                time.sleep(5)
                            
                            # Attempts to get phone and owner data from the page
                            try:
                                pw = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/main/div[2]/div[1]/div[2]/div/div[1]/div/div/div[4]/a')
                                phone_write = pw.text
                            except NoSuchElementException:
                                phone_write = ""
                            try:
                                nw = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/main/div[3]/div/div/div[1]/div/div[2]/div/div[1]/div/ul[2]/li/span')
                                name_write = nw.text
                            except NoSuchElementException:
                                name_write = ""
                            print(phone_write)
                            print(name_write)
                            
                            # Writes the results to the output csv
                            csv_writer.writerow(
                                [business_write, address_write, name_write, phone_write])
                            break
                        except NoSuchElementException:
                            print("Could not enter")
                    current_address_index += 2
    csv_output.close()
