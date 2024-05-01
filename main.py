"""This file will run to execute all the logics and ands"""
import undetected_chromedriver as uc
import time

from db import profiles_db
from page import LoginPage, TUPage, EURPage

"""
STEP 0: Initialize driver
"""
options = uc.ChromeOptions()
options.headless = False
driver = uc.Chrome(options=options,version_main=122)
pre_seed = False

"""
STEP 1: Login to LinkedIn
"""
login = LoginPage(driver, pre_seed)
driver.get(login.url)
login.login("o.dorhoutmees@gmail.com", "u7*Js,XcfE$7ccv")

"""
STEP 2: Scrape TU Delft
"""
tu = TUPage(driver, pre_seed)
driver.get(tu.url)
tu.scrape()
tu.persist()
tu.close()


"""
STEP 3: Scrape EUR
"""
eur = EURPage(driver, pre_seed)
driver.get(eur.url)
eur.scrape()
eur.persist()
eur.close()

"""
STEP 4: Close
"""
driver.close()


print("DONE!")