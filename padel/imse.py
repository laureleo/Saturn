from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import logging
import sys
from bs4 import BeautifulSoup
from datetime import datetime  
from datetime import timedelta 
from pyvirtualdisplay import Display
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.message import EmailMessage

from selenium.common.exceptions import NoSuchElementException    

from assets.creds_m import *
HOME = '/home/vic/git/Saturn/padel/'
weekday_mapper = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}


def element_exists(driver, tag, attribute_name, attribute_value):
    css_selector = f"{tag}[{attribute_name}='{attribute_value}']"

    try:
        driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True


def log_setup():
    logging.basicConfig(level=logging.INFO,
                        format='Imselog: %(asctime)s \n%(message)s')

    a_logger = logging.getLogger()
    
    #The logging setup persists in jupyter, so just a check so we don't keep on adding handlers ad infinitum!
    if len(a_logger.handlers) <= 1:
        # Get log messages to file
        output_file_handler = logging.FileHandler(f"{HOME}output.log", mode='w')
        a_logger.addHandler(output_file_handler)

        # Get log messages to stdout
        # stdout_handler = logging.StreamHandler(sys.stdout)
        #a_logger.addHandler(stdout_handler)
    return a_logger
    
    
def send_email():
    msg = EmailMessage()

    with open(f'{HOME}output.log') as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())

    msg['Subject'] = "Imse Report"
    msg['From'] = "Imse"
    msg['To'] = uname

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()


def imse_act(a_logger):
    today = datetime.today()
    then = today + timedelta(days=14)

    a_logger.info(f"It is {weekday_mapper[today.weekday()]}!\nImse is waking up, acting on (alias) {alias}s behalf\n")
    year = then.year
    month = then.month
    day = then.day
    book_url = f"""
    https://www.matchi.se/facilities/nynashamnpadelcenter?date={year}-{month}-{day}&sport=
    """

    login_url = "https://www.matchi.se/login/auth?returnUrl=%2Ffacilities%2Fnynashamnpadelcenter"

    a_logger.debug(f"Logging in at {login_url}...")
    a_logger.debug(f"Moving to the correct date at {book_url}...")
    d = Display(visible=0, size=(2560, 1440))
    d.start()

    try:
        a_logger.info(f"Despite being sleepy, Imse got up from his bed at {str(datetime.now())}")
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
        a_logger.info(f"On unsteady legs, Imse found himself at MATCHi at  {str(datetime.now())}")

        driver.get(book_url)
        driver.fullscreen_window()

        a_logger.info(f"Through bleary eyes, Imse started looking for free timeslots on {str(then)[:10]}...")
        soup = BeautifulSoup(driver.page_source, 'lxml')

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
        a_logger.info(f"There, his tired spider eyes saw \n\n{slots[['NAME','START','END']]}\n\n...but which to pick?")

        #time_priority = ['15:00', '16:00', '14:00']
        time_priority = ['18:00', '18:30', '17:30']
        DONE = 0
        for i, p in enumerate(time_priority):
            if DONE == 0:
                matched_slots = slots[slots['START'] == p].shape[0]
                a_logger.info(f"Imse searched for priority {i + 1} timeslots, ({p}), and found {matched_slots} possibilities")

                if matched_slots > 0:
                    for slot_index in range(matched_slots):
                        selected_booking_data = slots[slots['START'] == p].iloc[slot_index]
                        a_logger.info(f"Feeling a burst of energy, Imse goes for the kill and tries to book {selected_booking_data[1]} at {selected_booking_data[2]}!")
                        SELECTED_ID = selected_booking_data.SLOT_ID
                        try:
                            selected_slot = driver.find_element_by_css_selector(f"td[slotid='{SELECTED_ID}']")

                            driver.save_screenshot(f"{HOME}imse_{str(datetime.now())}.png")
                            selected_slot.click()                        
                            # This is where the capctcha can appear

                            tag = 'div'
                            attribute_name = 'class'
                            attribute_value = 'g-recaptcha'
                            css_selector = f"{tag}[{attribute_name}='{attribute_value}']"
                            if element_exists(driver, tag, attribute_name, attribute_value):
                                a_logger.info("GASP! A captcha tries to catch Imse")
                                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

                                try:
                                    captcha = driver.find_element_by_css_selector(css_selector)
                                    captcha.click()
                                    a_logger.info("...but Imse was too fast")

                                except Exception as e:
                                    a_logger.info(f"--- and captchured Imse :( \n{e}")


                            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'btnSubmit')))
                            driver.find_element_by_id('btnSubmit').click()
                            a_logger.info(f" Imse made the booking attempt {(datetime.now() - today).seconds} seconds after waking up...")

                            a_logger.info("...And he made it!")
                            DONE = 1
                            break
                        except Exception as e:
                            a_logger.warning(f"Imse couldn't book that, so he gathers this courage for a new attempt... {e}")

        if DONE == 0:
            a_logger.info("Imse seems to have failed. He is sorry to have dissapointed you, and promises to do better next time")
        else:
            a_logger.info("Blissfully happy, Imse went back to sleep with a light spider heart")

    except Exception as e:
        a_logger.warning(f"Imse was Vimse and fell down the drain : / {e}")

    driver.close()
    d.stop()
logger = log_setup()
imse_act(logger)
send_email()
