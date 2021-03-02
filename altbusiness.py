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

if __name__ == '__main__':

    # Opens the csv business input file
    with open('WorkDatabaseParsetoCSV.csv') as csv_input:
        company_as_list = []
        address_as_list = []
        # Parses each line with ',' as the delimiter
        # business_input = csv.reader(csv_input, delimiter=',')
        # business_input = csv.reader(csv_input)
        read_index = 0
        # for current_line in business_input:
        for current_line in csv_input:
            temp_list = current_line.split(",")
            # replaced_chars = temp_list[0].replace(' ', '-')
            # company_as_list.append(replaced_chars)
            company_as_list.append(temp_list[0])
            address_as_list.append(temp_list[1].rstrip('\n'))
            # print(company_as_list[read_index])
            # print(address_as_list[read_index])
            read_index += 1
        total_inputs = int(len(company_as_list))
    csv_input.close()

    # Opens the csv business output file
    with open('infooutput2.csv', mode='w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        options = Options()
        options.headless = False
        driver = webdriver.Chrome(executable_path=r'C:\Users\G\PycharmProjects\pythonProject\venv\chromedriver.exe',
                                  options=options)

        # Main scraping loop  \total_inputs
        for current_business in range(0, total_inputs):
            prompted = 0
            time.sleep(randint(1, 5))
            driver.get("https://www.bbb.org/")
            driver.maximize_window()

            time.sleep(randint(5, 8))
            insert_business_name = company_as_list[current_business]
            business_name_inputbox = driver.find_element_by_xpath('//*[@id="findTypeaheadInput"]')
            business_name_inputbox.send_keys(insert_business_name)

            time.sleep(randint(3, 5))
            clear_input_bin = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div/div[2]/div/form/div[2]/div[2]/button')
            # clear_input_bin = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div/header/section/div[3]/div/form/div[2]/div[2]/button')
            clear_input_bin.click()
            business_area_inputbox = driver.find_element_by_xpath('//*[@id="nearTypeaheadInput"]')
            business_area_inputbox.send_keys('Phoenix, AZ')

            time.sleep(randint(1, 5))
            search_box = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[2]/div[2]/div/div/div[2]/div/form/div[2]/button')
            # search_box = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[1]/div/header/section/div[3]/div/form/div[2]/button')
            search_box.click()

            time.sleep(randint(1, 5))

            try:
                clickable_btn = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/div[2]/fieldset/div[1]/label[2]/div/span/span[1]/input')
                print("Prompt box")
                clickable_btn.click()
                prompted = 1
            except NoSuchElementException:
                print("No prompt box")

            # Page loop
            total_nums = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[1]/h2/strong[1]'
            try:
                current_total = driver.find_element_by_xpath(total_nums).text
                max_number = int(current_total)
            except NoSuchElementException:
                max_number = 0
            # parse_ints = current_total
            # if parse_ints.isdigit():
            print(max_number)
            if max_number > 0:
                if max_number > 15:
                    max_number = 15
                current_address_index = 4
                for index in range(0, max_number):
                    business_address_return1 = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[%s]/div/div/div[2]/div[1]/p[2]'
                    business_address_return2 = '//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[%s]/div/div/div[2]/div[1]/p[3]'
                    bar1 = business_address_return1 % current_address_index
                    bar2 = business_address_return2 % current_address_index
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
                        # print(found_address)
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
                            # click_get_bus_info = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/main/div[2]/div[2]/div/div[4]/div[4]/div')
                            click_get_bus_info.click()
                            time.sleep(5)
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
                            csv_writer.writerow(
                                [business_write, address_write, name_write, phone_write])
                            break
                        except NoSuchElementException:
                            print("Could not enter")
                    current_address_index += 2
            # else:
                # business_write = company_as_list[current_business]
                # address_write = address_as_list[current_business]
                # csv_writer.writerow(
                    # [business_write, address_write, 'nodata', 'nodata'])
    csv_output.close()
