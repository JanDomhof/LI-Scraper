"""This file will run to execute all the logics and ands"""
import undetected_chromedriver as uc
from page import LoginPage, UNIPage, BigUNIPage
from resources import UNI
import os
import numpy as np
import time, datetime
from dotenv import load_dotenv
from tabulate import tabulate
load_dotenv()

# Loop indefinately
while True:
    start_time_total = time.time()
    """
    STEP 0: Initialize driver
    """
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-search-engine-choice-screen")
    driver = uc.Chrome(options=options,version_main=129)


    """
    STEP 1: Login to LinkedIn
    """
    login = LoginPage(driver)
    driver.get(login.url)
    login.login(os.environ["LI_USERNAME"], os.environ["LI_PASSWORD"])

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

    # some uni's result in more than 1000 profiles (which is the max load capacity on linkedin)
    # those are BigUNI objects where we filter on segments of start and end year to find all the results.
    unis = [
        UNI(name="TU Delft", url="https://www.linkedin.com/school/tudelft/people/", big=True),
        UNI(name="TU Delft | Electrical Engineering, Mathematics and Computer Science", url="https://www.linkedin.com/company/tu-delft-electrical-engineering-mathematics-and-computer-science/people/"),
        UNI(name="TU Delft | Applied Sciences", url="https://www.linkedin.com/company/tu-delft-applied-sciences/people/"),
        UNI(name="TU Delft | Aerospace Engineering", url="https://www.linkedin.com/company/tu-delft-aerospace-engineering/people/"),
        UNI(name="TU Delft | Civil Engineering and Geosciences", url="https://www.linkedin.com/school/tu-delft-civil-engineering-geosciences/people/", big=True),
        UNI(name="TU Delft | Mechanical Engineering", url="https://www.linkedin.com/school/tu-delft-mechanical-engineering/people/", big=True),
        UNI(name="TU Delft | Technology, Policy and Management", url="https://www.linkedin.com/school/tu-delft-technology-policy-and-management/people/", big=True),
        UNI(name="TU Delft | Industrial Design Engineering", url="https://www.linkedin.com/school/idetudelft/people/", big=True),
        UNI(name="Erasmus University", url="https://www.linkedin.com/school/erasmus-university-rotterdam/people/", big=True),
        UNI(name="Erasmus School of Accounting & Assurance", url="https://www.linkedin.com/school/erasmus-school-of-accounting-assurance-registercontroller/people/"),
        UNI(name="Erasmus School of Philosophy", url="https://www.linkedin.com/company/erasmus-school-of-philosophy/people/"),
        UNI(name="Erasmus School of History, Culture and Communication", url="https://www.linkedin.com/school/erasmus-school-of-history-culture-and-communication-eshcc/people/"),
        UNI(name="Erasmus School of Social and Behavioural Sciences", url="https://www.linkedin.com/school/erasmus-school-of-social-and-behavioural-sciences-essb/people/"),
        UNI(name="Erasmus School of Health Policy & Management", url="https://www.linkedin.com/company/erasmus-school-of-health-policy-&-management/people/"), 
        UNI(name="Erasmus School of Law", url="https://www.linkedin.com/school/erasmus-school-of-law/people/", big=True),
        UNI(name="Erasmus School of Economics", url="https://www.linkedin.com/school/erasmus-school-of-economics/people/", big=True),
        UNI(name="Erasmus Rotterdam School of Management", url="https://www.linkedin.com/school/rotterdam-school-of-management-erasmus-university/people/", big=True),
    ]

    """
    STEP 3: SCRAPE!!!
    """
    uni_pages = []
    for u in unis:
        if u.big:
            uni_page = BigUNIPage(driver=driver, pre_seed=True, url=u.url, name=u.name)
        else:
            uni_page = UNIPage(driver=driver, pre_seed=True, url=u.url, name=u.name)
        uni_pages.append(uni_page)
        uni_page.scrape()
        uni_page.close()
        # try:
                
        # except Exception as e:
        #     print(f"Error with scraper for {u.name}:\n{e}")

    """
    STEP 4: Close driver
    """
    driver.close()

    """
    STEP 5: Create report
    """
    # create a table for the reports and total reports for each scraper
    reports_table = [u.get_report_table()[-1] for u in uni_pages]
    for i, r in enumerate(reports_table):
        r[0] = uni_pages[i].uni

    # get the TOTAL row from each uni report, and sum them to get a TOTAL TOTAL
    totals = np.array([u.get_report_table()[-1][3:] for u in uni_pages]).astype(int)
    totals_sums = np.sum(totals, axis=0)
    
    # create new row for total scores and add the column sums
    total_row = ['TOTAL','','']
    total_row.extend(totals_sums)

    # add a row that indicates a seperation and then the TOTAL row
    reports_table.append(['--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +'])
    reports_table.append(total_row)

    report = ""
    report += f"LinkedIn scraper report!"
    report += f"Timestamp: {datetime.datetime.now().strftime('%c')}\n\n"
    report += f"{tabulate(reports_table, headers=['University Page Name', '','', 'Count on page', 'Profiles found', 'New', 'New title', 'Old', 'Error', 'Outside connection range', 'Scrolls'], tablefmt='orgtbl')}\n\n\n"
    report += f"Below is a report for every UNI page:\n\n"
    for u in uni_pages:
        report += u.get_report()
        report += "\n\n"

    with open(f'./reports/{time.strftime("%Y%m%d-%H%M%S")}.txt', "w") as writer:
        writer.write(report)