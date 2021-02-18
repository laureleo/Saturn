from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import logging
from bs4 import BeautifulSoup
from datetime import datetime  
from datetime import timedelta 
from pyvirtualdisplay import Display
import random


weekday_mapper = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

from assets.creds_m import *

#logging.basicConfig(filename='imse.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)

today = datetime.today()
then = today + timedelta(days=14)

logging.info(f"It is {weekday_mapper[today.weekday()]}!\nImse is waking up, acting on (alias) {alias}s behalf\n")
year = then.year
month = then.month
day = then.day
book_url = f"""
https://www.matchi.se/facilities/nynashamnpadelcenter?date={year}-{month}-{day}&sport=
"""

login_url = "https://www.matchi.se/login/auth?returnUrl=%2Ffacilities%2Fnynashamnpadelcenter"

logging.debug(f"Logging in at {login_url}...")
logging.debug(f"Moving to the correct date at {book_url}...")
d = Display(visible=0, size=(2560, 1440))
d.start()

try:
    logging.info(f"Despite being sleepy, Imse got up from his bed at {str(datetime.now())}")
    driver = webdriver.Firefox()
    driver.get(login_url)
    assert driver.title == 'Login - MATCHi'

    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(uname)

    password = driver.find_element_by_name("j_password")
    password.clear()
    password.send_keys(pwd)

    driver.find_element_by_xpath('//*[@id="loginForm"]/button').click()
    logging.info(f"On unsteady legs, Imse found himself at MATCHi at  {str(datetime.now())}")

    driver.get(book_url)
    driver.fullscreen_window()
    driver.save_screenshot(f"/home/vic/git/Saturn/padel/imsse_{str(datetime.now())}.png")



    
    logging.info(f"Through bleary eyes, Imse started looking for free timeslots at {str(then)[:10]}...")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #time.sleep(1)
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
    logging.debug(f"Found {slots}")
    logging.info(f"There, his tired spider eyes saw \n\n{slots[['NAME','START','END']]}\n\n...but which to pick?")

    #time_priority = ['15:00', '16:00', '14:00']
    time_priority = ['18:00', '18:30', '17:30']
    DONE = 0

    for i, p in enumerate(time_priority):
        if DONE == 0:
            matched_slots = slots[slots['START'] == p].shape[0]
            logging.info(f"Imse searched for priority {i + 1} timeslots, ({p}), and found {matched_slots} possibilities")

            if matched_slots > 0:
                for slot_index in range(matched_slots):
                    selected_booking_data = slots[slots['START'] == p].iloc[slot_index]
                    logging.info(f"Feeling a burst of energy, Imse goes for the kill and tries to book {selected_booking_data[1]} at {selected_booking_data[2]}!")
                    SELECTED_ID = selected_booking_data.SLOT_ID
                    try:
                        selected_slot = driver.find_element_by_css_selector(f"td[slotid='{SELECTED_ID}']")
                        
                        driver.save_screenshot(f"/home/vic/git/Saturn/padel/imsse_{str(datetime.now())}.png")
                        selected_slot.click()
                        time.sleep(random.uniform(1,5))
                        logging.info(f"Imse made the booking attempt {(datetime.now() - today).seconds} seconds after waking up...")

                        driver.find_element_by_id('btnSubmit').click()
                        logging.info("...And he made it!")
                        DONE = 1
                        break
                    except Exception as e:
                        logging.warning(f"But Imse couldn't book that for some reason, so he gathers  his courage for a new attempt... {e}")

    if DONE == 0:
        logging.info("Imse seems to have failed. He is sorry to have dissapointed you, and promises to do better next time")
    else:
        logging.info("Blissfully happy, Imse went back to sleep with a light spider heart")

except Exception as e:
    logging.warning(f"Imse was Vimse and fell down the drain : / {e}")

driver.close()
d.stop()
