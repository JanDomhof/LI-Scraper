"""This file will run to execute all the logics and ands"""
import undetected_chromedriver as uc
from page import LoginPage, UNIPage
from resources import UNI
import os
import numpy as np
import time, datetime
from dotenv import load_dotenv
from tabulate import tabulate
load_dotenv()

# Loop indefinately
report_count = max([int(f.split(" ")[-1].split(".")[0]) for f in os.listdir("./reports")])
while True:
    start_time_total = time.time()
    report_count += 1
    """
    STEP 0: Initialize driver
    """
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-search-engine-choice-screen")
    driver = uc.Chrome(options=options,version_main=127)


    """
    STEP 1: Login to LinkedIn
    """
    login = LoginPage(driver)
    driver.get(login.url)
    login.login(os.environ["LI_USERNAME"], os.environ["LI_PASSWORD"])
    time.sleep(10)

    """
    STEP 2: UNIs list
    """
    # The uni pages below have no founder employees and <20 members. No need to scrape them
    bad_unis = [
        # UNI(name="TU Delft | AI", url="https://www.linkedin.com/showcase/tudelftai/"),
        # UNI(name="TU Delft | Global Initiative", url="https://www.linkedin.com/showcase/tu-delft-global-initiative/people/"),
        # UNI(name="TU Delft Corporate Innovation", url="https://www.linkedin.com/company/tud-ci/people/"),
        # UNI(name="TU Delft Energy Initiative", url="https://www.linkedin.com/company/tu-delft-energy-initiative/people/"),
        # UNI(name="TU Delft Swarming Lab", url="https://www.linkedin.com/company/tu-delft-swarming-lab/people/"),
        # UNI(name="TU Delft Campus", url="https://www.linkedin.com/company/tudelftcampus/people/"),
        # UNI(name="TU Delft Wind Energy Institute", url="https://www.linkedin.com/company/tudelftwindenergyinstitute/people/"),
        # UNI(name="Erasmus MC Graduate School", url="https://www.linkedin.com/company/erasmus-mc-graduate-school/people/"),
    ]

    # some uni's have an option to select startyear and endyear in the filters
    # those are made twice, once for pre-seed, once for seed
    unis = [
        UNIPage(driver=driver, pre_seed=True, name="TU Delft", url="https://www.linkedin.com/school/tudelft/people/"),
        UNIPage(driver=driver, pre_seed=False, name="TU Delft", url="https://www.linkedin.com/school/tudelft/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Electrical Engineering, Mathematics and Computer Science", url="https://www.linkedin.com/company/tu-delft-electrical-engineering-mathematics-and-computer-science/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Applied Sciences", url="https://www.linkedin.com/company/tu-delft-applied-sciences/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Aerospace Engineering", url="https://www.linkedin.com/company/tu-delft-aerospace-engineering/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Civil Engineering and Geosciences", url="https://www.linkedin.com/school/tu-delft-civil-engineering-geosciences/people/"),
        UNIPage(driver=driver, pre_seed=False, name="TU Delft | Civil Engineering and Geosciences", url="https://www.linkedin.com/school/tu-delft-civil-engineering-geosciences/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Mechanical Engineering", url="https://www.linkedin.com/school/tu-delft-mechanical-engineering/people/"),
        UNIPage(driver=driver, pre_seed=False, name="TU Delft | Mechanical Engineering", url="https://www.linkedin.com/school/tu-delft-mechanical-engineering/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Technology, Policy and Management", url="https://www.linkedin.com/school/tu-delft-technology-policy-and-management/people/"),
        UNIPage(driver=driver, pre_seed=False, name="TU Delft | Technology, Policy and Management", url="https://www.linkedin.com/school/tu-delft-technology-policy-and-management/people/"),
        UNIPage(driver=driver, pre_seed=True, name="TU Delft | Industrial Design Engineering", url="https://www.linkedin.com/school/idetudelft/people/"),
        UNIPage(driver=driver, pre_seed=False, name="TU Delft | Industrial Design Engineering", url="https://www.linkedin.com/school/idetudelft/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus University", url="https://www.linkedin.com/school/erasmus-university-rotterdam/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus University", url="https://www.linkedin.com/school/erasmus-university-rotterdam/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Accounting & Assurance", url="https://www.linkedin.com/school/erasmus-school-of-accounting-assurance-registercontroller/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus School of Accounting & Assurance", url="https://www.linkedin.com/school/erasmus-school-of-accounting-assurance-registercontroller/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Philosophy", url="https://www.linkedin.com/company/erasmus-school-of-philosophy/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of History, Culture and Communication", url="https://www.linkedin.com/school/erasmus-school-of-history-culture-and-communication-eshcc/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus School of History, Culture and Communication", url="https://www.linkedin.com/school/erasmus-school-of-history-culture-and-communication-eshcc/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Social and Behavioural Sciences", url="https://www.linkedin.com/school/erasmus-school-of-social-and-behavioural-sciences-essb/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus School of Social and Behavioural Sciences", url="https://www.linkedin.com/school/erasmus-school-of-social-and-behavioural-sciences-essb/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Health Policy & Management", url="https://www.linkedin.com/company/erasmus-school-of-health-policy-&-management/people/"), 
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Law", url="https://www.linkedin.com/school/erasmus-school-of-law/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus School of Law", url="https://www.linkedin.com/school/erasmus-school-of-law/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus School of Economics", url="https://www.linkedin.com/school/erasmus-school-of-economics/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus School of Economics", url="https://www.linkedin.com/school/erasmus-school-of-economics/people/"),
        UNIPage(driver=driver, pre_seed=True, name="Erasmus Rotterdam School of Management", url="https://www.linkedin.com/school/rotterdam-school-of-management-erasmus-university/people/"),
        UNIPage(driver=driver, pre_seed=False, name="Erasmus Rotterdam School of Management", url="https://www.linkedin.com/school/rotterdam-school-of-management-erasmus-university/people/"),
    ]

    """
    STEP 3: SCRAPE!!!
    """
    for u in unis:
        try:
            u.scrape()
            u.close()
        except Exception as e:
            print(f"Error with scraper for {u.uni}:\n{e}")


    """
    STEP 4: Close driver
    """
    driver.close()

    """
    STEP 5: Create report
    """
    # create a table for the reports and total reports for each scraper
    reports_table = [u.get_report_table()[-1] for u in unis]
    for i, r in enumerate(reports_table):
        r[0] = unis[i].uni

    # get the TOTAL row from each uni report, and sum them to get a TOTAL TOTAL
    totals = np.array([u.get_report_table()[-1][1:] for u in unis]).astype(int)
    totals_sums = np.sum(totals, axis=0)
    
    # create new row for total scores and add the column sums
    total_row = ['TOTAL']
    total_row.extend(totals_sums)

    # add a row that indicates a seperation and then the TOTAL row
    reports_table.append(['--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +'])
    reports_table.append(total_row)

    with open(f"./reports/Scraper report {report_count}.txt", "w") as report:
        report.write(f"Scraper report nr. {report_count}\n\n")
        report.write(f"Timestamp: {datetime.datetime.now().strftime('%c')}\n\n")
        report.write(f"{tabulate(reports_table, headers=['University Page Name', 'Count on page', 'Profiles found', 'New', 'New title', 'Old', 'Error', 'Outside connection range', 'Scrolls'], tablefmt='orgtbl')}\n\n\n")
        report.write(f"Below is a report for every UNI page:\n\n")
        for u in unis:
            report.write(u.get_report())
            report.write("\n\n")
    