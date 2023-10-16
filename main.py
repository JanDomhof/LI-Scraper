"""This file will run to execute all the logics and commands"""
import undetected_chromedriver as uc
import time

from db import profiles_db
from page import LoginPage, TUPage, EURPage

"""
STEP 0: Initialize driver
"""
driver = uc.Chrome(version_main=117)

"""
STEP 1: Login to LinkedIn
"""
login = LoginPage(driver)
driver.get(login.url)
login.login("j.h.domhof@outlook.com", "=ggB?^8fEWPz2t")

"""
STEP 2: Scrape TU Delft
"""
tu = TUPage(driver)
driver.get(tu.url)
founders = tu.scrape()

"""
STEP 3: Scrape EUR
"""
# eur = EURPage(driver)
# driver.get(eur.url)
# eur.scrape()

"""
STEP 4: Save to DB
"""
tu.persist()
# eur.persist()

"""
STEP 5: Close
"""
driver.close()
tu.close()
# eur.close()
