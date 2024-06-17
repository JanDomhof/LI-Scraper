"""This file will run to execute all the logics and ands"""
import undetected_chromedriver as uc
from page import LoginPage, TUPage, EURPage, UNIPage
from resources import UNI
import os
import time, datetime
from dotenv import load_dotenv
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
    driver = uc.Chrome(options=options,version_main=124)

    """
    STEP 1: Login to LinkedIn
    """
    login = LoginPage(driver, False)
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
    unis = [
        UNI(name="TU Delft", url="https://www.linkedin.com/school/tudelft/people/"),
        # UNI(name="TU Delft | Electrical Engineering, Mathematics and Computer Science", url="https://www.linkedin.com/company/tu-delft-electrical-engineering-mathematics-and-computer-science/people/", year_option=False),
        # UNI(name="TU Delft | Applied Sciences", url="https://www.linkedin.com/company/tu-delft-applied-sciences/people/", year_option=False),
        # UNI(name="TU Delft | Aerospace Engineering", url="https://www.linkedin.com/company/tu-delft-aerospace-engineering/people/", year_option=False),
        # UNI(name="TU Delft | Civil Engineering and Geosciences", url="https://www.linkedin.com/school/tu-delft-civil-engineering-geosciences/people/"),
        # UNI(name="TU Delft | Mechanical Engineering", url="https://www.linkedin.com/school/tu-delft-mechanical-engineering/people/"),
        # UNI(name="TU Delft | Technology, Policy and Management", url="https://www.linkedin.com/school/tu-delft-technology-policy-and-management/people/"),
        # UNI(name="TU Delft | Industrial Design Engineering", url="https://www.linkedin.com/school/idetudelft/people/"),
        # UNI(name="Erasmus University", url="https://www.linkedin.com/school/erasmus-university-rotterdam/people/"),
        # UNI(name="Erasmus School of Accounting & Assurance", url="https://www.linkedin.com/school/erasmus-school-of-accounting-assurance-registercontroller/people/"),
        # UNI(name="Erasmus School of Philosophy", url="https://www.linkedin.com/company/erasmus-school-of-philosophy/people/", year_option=False),
        # UNI(name="Erasmus School of History, Culture and Communication", url="https://www.linkedin.com/school/erasmus-school-of-history-culture-and-communication-eshcc/people/"),
        # UNI(name="Erasmus School of Social and Behavioural Sciences", url="https://www.linkedin.com/school/erasmus-school-of-social-and-behavioural-sciences-essb/people/"),
        # UNI(name="Erasmus School of Health Policy & Management", url="https://www.linkedin.com/company/erasmus-school-of-health-policy-&-management/people/", year_option=False), 
        # UNI(name="Erasmus School of Law", url="https://www.linkedin.com/school/erasmus-school-of-law/people/"),
        # UNI(name="Erasmus School of Economics", url="https://www.linkedin.com/school/erasmus-school-of-economics/people/"),
        # UNI(name="Erasmus Rotterdam School of Management", url="https://www.linkedin.com/school/rotterdam-school-of-management-erasmus-university/people/"),
    ]

    """
    STEP 3: SCRAPE!!!
    """
    for u in unis:
        try:
            start_time = time.time()
            # Scrape uni for pre-seed
            uni_pre_seed = UNIPage(driver=driver, pre_seed=True, url=u.url, name=u.name)
            uni_pre_seed.scrape()
            uni_pre_seed.persist()
            uni_pre_seed.close()

            # Set pre-seed report
            u.set_pre_seed_report(runtime=(time.time() - start_time) / 60,
                                total=uni_pre_seed.report_total,
                                new=uni_pre_seed.report_new,
                                new_title=uni_pre_seed.report_new_title,
                                old=uni_pre_seed.report_old,
                                error=uni_pre_seed.report_error)

            start_time = time.time()
            # Scrape uni for seed
            uni_seed = UNIPage(driver=driver, pre_seed=False, url=u.url, name=u.name)
            if u.year_option:
                uni_seed.scrape()
                uni_seed.persist()
                uni_seed.close()

            # Set seed report
            u.set_seed_report(runtime=(time.time() - start_time) / 60,
                                total=uni_seed.report_total,
                                new=uni_seed.report_new,
                                new_title=uni_seed.report_new_title,
                                old=uni_seed.report_old,
                                error=uni_seed.report_error)
        except Exception as e:
            print(f"Error with scraper for: {u.name}\n{e}")


    """
    STEP 4: Close driver
    """
    driver.close()

    """
    STEP 5: Create report:
                - Total time
                - Total amount of profiles found, divided into:
                    - Amount of new profiles found
                    - Amount of already known profiles found
                    - Amount of already known profiles with a changed title
                - For every uni:
                    - Total time
                    - Total amount of profiles found, divided into:
                        - Amount of new profiles found
                        - Amount of already known profiles found
                        - Amount of already known profiles with a changed title
    """
    report_total = sum([u.pre_seed_total + u.seed_total for u in unis])
    report_new = sum([u.pre_seed_new + u.seed_new for u in unis])
    report_new_title = sum([u.pre_seed_new_title + u.seed_new_title for u in unis])
    report_old = sum([u.pre_seed_old + u.seed_old for u in unis])
    report_error = sum([u.pre_seed_error + u.seed_error for u in unis])

    with open(f"./reports/Scraper report {report_count}.txt", "w") as report:
        report.write(f"Scraper report nr. {report_count}\n\n")
        report.write(f"Timestamp: {datetime.datetime.now().strftime('%c')}")
        report.write(f"""
Found a total of {report_total} profiles in {(time.time() - start_time_total) / 60 / 60} hours:
Nr of new profiles: {report_new}
Nr of profiles with a new title: {report_new_title}
Nr of already known profiles: {report_old}
Nr of errors: {report_error}

""")
        report.write(f"Below is a report for every UNI page:\n")
        for u in unis:
            report.write(u.get_report())
    