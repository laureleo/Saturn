#!/usr/bin/python2.7
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import logging
from bs4 import BeautifulSoup
from datetime import datetime  
from datetime import timedelta  

logging.basicConfig(filename='imse.log', level=logging.INFO)
#logging.basicConfig(level=logging.INFO)



today = datetime.today()
then = today + timedelta(days=14)

logging.info(f"Today is {str(today)[:10]}. I'm going to check {str(then)[:10]} for free slots!")

year = then.year
month = then.month
day = then.day
book_url = f"""
https://www.matchi.se/facilities/nynashamnpadelcenter?date={year}-{month}-{day}&sport=
"""

login_url = "https://www.matchi.se/login/auth?returnUrl=%2Ffacilities%2Fnynashamnpadelcenter"

logging.info(f"Logging in at {login_url}...")
logging.info(f"Moving to the correct date at {book_url}...")

try:
    logging.info(f"IMSE ACTIVATED AT {str(datetime.now())}")
    driver = webdriver.Chrome()
    driver.get(login_url)
    assert driver.title == 'Login - MATCHi'
    logging.info("Logging in...")

    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys("Leoctio@gmail.com")

    password = driver.find_element_by_name("j_password")
    password.clear()
    password.send_keys("ignotus")

    driver.find_element_by_xpath('//*[@id="loginForm"]/button').click()
    time.sleep(1)

    driver.get(book_url)
    driver.fullscreen_window()

    time.sleep(1)
    logging.info("Looking for free slots...")


    soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(1)
    schedule = soup.find('div', attrs = {'class': 'schedule'})
    free = schedule.find_all('td', attrs = {'class': 'slot free'})
    
    slots = pd.DataFrame()
    for i, f in enumerate(free):
        slot_id = f['slotid']
        slot_title = f['data-original-title']
        slot_availability, slot_lane, slot_time = slot_title.split(sep='<br>')
        status, name, slottime = slot_title.split(sep ='<br>')
        _, start, _, end = slottime.split(sep = ' ')

        name = name.split(sep = '.')[1]

        slots.at[i, "SLOT_ID"] = slot_id
        slots.at[i, "NAME"] = name
        slots.at[i, "START"] = start
        slots.at[i, "END"] = end
    logging.info(f"Found {slots}")



    time_priority = ['15:00', '16:00','23:00', '14:00']

    for i, p in enumerate(time_priority):
        matched_slots = slots[slots['START'] == p].shape[0]
        logging.info(f"Looking at priority {i + 1} timeslot, {p}, and found {matched_slots} possibilities")

        if matched_slots > 0:
            selected_booking_data = slots[slots['START'] == '23:00'].iloc[0]
            logging.info(f"Selecting {selected_booking_data}")
            SELECTED_ID = selected_booking_data.SLOT_ID
            try:

                logging.info(f"Attempting to book {SELECTED_ID} at {str(datetime.now())}")

                selected_slot = driver.find_element_by_css_selector(f"td[slotid='{SELECTED_ID}']")
                selected_slot.click()
                time.sleep(1)
                driver.find_element_by_id('btnSubmit').click()

                time.sleep(1)

                payment_name = driver.find_element_by_xpath("//input[@placeholder='Card owner name']")
                payment_name.send_keys("El donatello")
            
                break;
            except Exception as e:
                logging.warn("Couln't book that, continuing... {e}")
                

    time.sleep(1)
    driver.close()
except Exception as e:
    logging.warning(f"Imse was Vimse and fell down the drain: / {e}")
    driver.close()
