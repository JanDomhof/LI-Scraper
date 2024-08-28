from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from resources import Selector, LoginPageResources, TUDelftResources, EURResources, UniPageResources
from typing import List
import contextlib, pyautogui, random, time, string, numpy as np
from tabulate import tabulate

from db import profiles_db
from edda import Edda

class BasePage:
    """Base class for all the pages
    the subclasses will contain all the methods can be perform on a
    single page

    you can start a new instance of this class as follow

    page = BasePage(driver)
    """
    def __init__(self, driver:Remote) -> None:
        self.driver: Remote = driver
        self.driver.maximize_window()

    def find(self, selector: Selector) -> WebElement:
        """This method will find and return an element from the driver"""
        return self.driver.find_element(selector.ST, selector.SP)

    def find_from_element(self, element: WebElement, selector: Selector) -> WebElement:
        """This method will find and return an element from another element"""
        return element.find_element(selector.ST, selector.SP)

    def find_all(self, selector: Selector) -> List[WebElement]:
        """This method will find and return a list of all available element from the driver"""
        return self.driver.find_elements(selector.ST, selector.SP)

    def wait_until_find(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_element_located) -> WebElement:
        """This method will wait for element to be present in DOM and return an available element from the driver"""
        return WebDriverWait(self.driver, timeout).until(condition((selector.ST, selector.SP)))

    def wait_until_find_all(self, selector: Selector, timeout: int = 10, condition=EC.presence_of_all_elements_located) -> List[WebElement]:
        """This method will wait for elements to be present in DOM and return a list of all available element from the driver"""
        return WebDriverWait(self.driver, timeout).until(condition((selector.ST, selector.SP)))
    
    def click(self, element: WebElement, doorgaan_button=False) -> None:
        """Will try to click the given element
        but if it fails it will run script to execute it"""
        if isinstance(element, WebElement):
            try:
                element.click()
            except Exception as e:
                self.driver.execute_script("arguments[0].click();", element)
    
    def click_all(self, elements: List[WebElement] ) -> None:
        for element in elements:
            self.click(element)

    def send_keys(self, element: WebElement, text: str) -> None:
        """This method will help to type text like human

        Args:
            element (WebElement): input element to send keys to
            text (str): text to send
        """
        element.clear()
        for letter in text:
            element.send_keys(letter)
        return element
        
    def random_mouse_movement(self, total_num):
        """
            It will randomly move mouse on the screen for specific number of times.
            Params:
                total_num : Number of times to do this random mouse movement (int)
        """
        # self.circular_mousemovement(random.randint(100, 300))
        for _ in range(total_num):
            width, height = pyautogui.size()

            random_width = random.randint(0, width - 1)
            random_height = random.randint(0, height - 1)
            self.move_mouse_to_coordinates(random_width, random_height)

    @staticmethod
    def move_mouse_to_coordinates(x, y):
        """
            Will move mouse to respective coordinates
            Params:
                x (int value)
                y (int value)
        """
        time_to_move = random.uniform(0.1, 2.0)
        time_to_move = round(time_to_move, 1)

        """ Empty String so that linear mouse movement """
        movements = [pyautogui.easeInQuad, pyautogui.easeOutQuad, pyautogui.easeInOutQuad, pyautogui.easeInBounce, pyautogui.easeInElastic] # type: ignore
        pyautogui.FAILSAFE = False
        try:
            pyautogui.moveTo(x, y, time_to_move, random.choice(movements))
        # except InvalidCoordinatesException as e:
        except Exception as e:
            pyautogui.moveTo(x, y, time_to_move)
            # logging.info("Changing coordinates because of ", type(e))

    def move_mouse_to_element(self, element):
        """
            It will move the mouse cursor to the sepecific element displayed on the screen
            Params:
                driver (selenium webdriver object)
                element (selenium element)
        """
        actions = ActionChains(self.driver)

        panel_height = self.driver.execute_script('return window.outerHeight - window.innerHeight;')
        abs_x = element.location['x']
        y = element.location['y']
        abs_y = y + panel_height
        self.move_mouse_to_coordinates(abs_x, abs_y)
        actions.move_to_element(element)
        with contextlib.suppress(Exception):
            actions.perform()

    def find_and_click(self, selector: Selector, timeout: int = 10):
        element = self.scroll_to(selector, timeout)
        self.click(element)
        return element
    
    def scroll_to(self, selector: Selector, timeout: int = 10):
        element = self.wait_until_find(selector, timeout)
        with contextlib.suppress(Exception):
            scroll = ActionChains(self.driver)
            scroll.move_to_element(element).perform()
        return element

    def scroll_to_element(self, element: WebElement):
        with contextlib.suppress(Exception):
            scroll = ActionChains(self.driver)
            scroll.move_to_element(element).perform()
        return element
    
    def scrape_page(self, n_iter):
        scrolls = 0
        for i in range(n_iter):
            try:
                # if you scroll to the bottom of the page, a new batch of profiles will load
                show_more_button = self.wait_until_find(TUDelftResources.ShowMoreButton, 5)
                self.scroll_to_element(show_more_button)
            except:
                # if we are at the bottom, we save the amount of scrolls it took
                scrolls = i
                break

        try:
            # after scrolling to the bottom, we return all the founders on the page
            return self.wait_until_find_all(TUDelftResources.Founder, 10), scrolls
        except Exception as e:
            # if something goes wrong, print the error
            print(e)
            return [], 0

    def close(self):
        self.db.close()

class LoginPage (BasePage):
    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        self.url = LoginPageResources.URL

    def login(self, email: str, password: str):  
        self.driver.get(LoginPageResources.URL)  
          
        username_field = self.wait_until_find(LoginPageResources.UsernameField, 10)
        self.click(username_field)
        self.send_keys(username_field, email)

        password_field = self.wait_until_find(LoginPageResources.PasswordField, 10)
        self.click(password_field)
        self.send_keys(password_field, password)
        
        login_button = self.wait_until_find(LoginPageResources.LoginButton, 10)
        self.click(login_button)

        self.wait_until_find(LoginPageResources.ProfilePicture, 100)
        print("Logged in!")

class UNIPage (BasePage):
    def __init__(self, driver: Remote, pre_seed, url, name) -> None:
        super().__init__(driver)
        self.url = url
        self.uni = name
        self.db = profiles_db()
        self.edda = Edda()
        self.reports = []

        self.pre_seed = pre_seed
        if pre_seed:
            self.assignees = self.db.fetch_assignees(['Daan', 'Boaz', 'Ole', 'Jan', 'Tessa', 'Elsa', 'Robin', 'Rozanne', 'Sophie'])
        else:
            self.assignees = self.db.fetch_assignees(['Ileana', 'Jasper', 'Isabelle'])


    # first, we make all url possibilities
    # in these url's, you can already apply filters (e.g., keyword or start/end year)
    # most efficient way of filtering
    def create_urls(self, use_filters=True):
        base_url = self.url if self.url[-1] == '/' else self.url + '/'
        return [base_url]
    
    # strange looking function but it works. It removes all punctuation from a string.
    # this is used on the names and titles of linkedin profiles since some people have smileys or 
    # special characters that break the code when we make a query to the database.
    def remove_punctuation(self, text):
        return text.translate(str.maketrans(string.punctuation, ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")).replace(",", "")
    
    def scrape(self):
        # first we check how many alumni the page has. If that is less than 1000,
        # we don't have to filter on the results since we can view all the members by just scrolling down the page
        # This saves quite some time when scraping almost empty pages
        self.driver.get(self.url)
        alumni_count = int(self.remove_punctuation(self.wait_until_find(UniPageResources.MemberCountField).text.strip().split(' ')[0]))
        use_filters = alumni_count >= 1000

        # first, we make all url possibilities
        # in these url's, you can already apply filters (e.g., keyword or start/end year)
        urls = self.create_urls(use_filters)

        for url in urls:
            # fetch the page
            self.driver.get(url)

            # see how many profiles there are in this filter
            member_count = int(self.remove_punctuation(self.wait_until_find(UniPageResources.MemberCountField).text.strip().split(' ')[0]))

            # scrape the page
            founder_elements, scrolls = self.scrape_page(n_iter=10)

            # fetch all names and titles from the database
            try:
                db_records = self.db.fetch_name_li_title()
            except:
                # if fails, reopen connection and do again
                self.db.open_connection()
                db_records = self.db.fetch_name_li_title()

            # define founder list and counts for this batch
            batch_founders_list = []
            batch_total = len(founder_elements)
            batch_new = 0
            batch_new_title = 0
            batch_old = 0
            batch_error = 0
            batch_fouth_connection = 0

            # for every profile we have found during scraping
            for founder in founder_elements:
                # get name, linkedin, title
                try:
                    name = self.remove_punctuation(self.find_from_element(founder, TUDelftResources.FounderName).text.strip())
                    linkedin = self.find_from_element(founder, TUDelftResources.FounderLink).get_attribute("href").split("?")[0]
                    title = self.remove_punctuation(self.find_from_element(founder, TUDelftResources.FounderTitle).text.strip())
                # if something goes wrong in fetching the above, we add 1 to the error counter and move to the next profile
                except:
                    batch_error += 1
                    continue
                
                # if we cannot view the name of this person (i.e. 4+ cirkel connectie waardoor hij 'LinkedIn Member' als naam heeft)
                if (
                        name == "LinkedIn Member"
                    ):
                    batch_fouth_connection += 1
                    continue

                # if this linkedin profile is already in the db, we have found a 'known' profile
                if (   
                        db_records['Linkedin'].str.contains(linkedin).any()
                    ):
                    # if name or title has changed, the profile might have changed job or positions (might have become a founder recently!!)
                    # if so, we change the title and set checked to 0 so that it reappears in the scrape tool
                    if (
                            not name == self.db.fetch_name(linkedin) or
                            not title == self.db.fetch_title(linkedin)
                        ):
                        try:
                            self.db.update_record(name, title, linkedin)
                        except:
                            # if fails, reopen connection and try again
                            self.db.open_connection()
                            self.db.update_record(name, title, linkedin)
                        finally:
                            batch_new_title += 1

                    # if title has not changed, we already know this profile, so we add 1 to the old profile counter
                    else:
                        batch_old += 1

                    # we don't have to do anything else (either it is old, or we have updated the entry with the new title)
                    # so we continue to the next founder
                    continue

                # Since we have reached this part in the code we know 2 things:
                #   - the founder name and title were not already found in this batch
                #   - the founder name and title were not already in our database
                # 
                # So we found a new profile!!! We try to fetch all data and create new founder.
                try:
                    batch_founders_list.append({
                        "Name": name,
                        "Linkedin": linkedin,
                        "Title": title,
                        "University": self.uni,
                        "Year": None, # deze moet eigenlijk weg, hebben niet echt een manier om dit te checken
                        "TitleIndicatesFounder": 1 if self.check_if_founder(self.find_from_element(founder, TUDelftResources.FounderTitle).text.lower().strip()) else 0,
                        "InEdda": 0, # deze moet nog geimplementeerd worden, zou kunnen door van elk bedrijf in edda de 'Founder' text field te getten en checken of de naam van deze founder daar in zit.
                        "MatchingEddaWord": "", # kan alleen als deze hierboven is gefixt (dan moet dit de naam van de startup zijn)
                        "Assignee": min(self.assignees, key=self.assignees.get),
                        "Checked": 0,
                        "AddedToEdda": 0,
                        "Vertical": None
                    })

                    # if we reach this part in the code, we know that:
                    #   - all the necessary information has been found succesfully
                    #   - a founder object has been created
                    # 
                    # so we can add 1 to the 'new founders' count and add a to the assignee counter (for workload distribution)
                    batch_new += 1
                    self.assignees[min(self.assignees, key=self.assignees.get)] += 1

                # if something went wrong with fetching the information above, there was an error.
                # we print the error so we can check later and add 1 to the error counter.
                except Exception as e:
                    print(e)
                    batch_error += 1
                    continue

            # if we have found a new profile:
            # persist these entries in the database and continue to the next url / filter
            if batch_new > 0:
                try:
                    self.db.insert(batch_founders_list)
                except:
                    self.db.open_connection()
                    self.db.insert(batch_founders_list)

            # create report for this filter for this uni page
            self.reports.append(
                [
                    url.split('=')[-1] if "=" in url else "No filter used", # keyword
                    url.split('=')[2][0:4], # start year
                    url.split('=')[1][0:4], # end year
                    member_count,
                    batch_total,
                    batch_new,
                    batch_new_title,
                    batch_old,
                    batch_error,
                    batch_fouth_connection,
                    scrolls
                ]
            )

            # this is for checking the terminal while the code is running (as you cannot see the report yet)
            print(self.get_report())

    def check_if_founder(self, title) -> bool:
        # these keywords are usually not founders
        bad_keyword_found = any(keyword in title for keyword in['consultant', 'consultancy', 'consulting', 'consult', 'consultation', 'strategy', 'strategic', 'art', 'arts', 'design', 'designer', 'studio', 'architect', 'architecture', 'law', 'lawyer'])
        
        # these keywords are usually founders
        good_keyword_found = any(keyword in title for keyword in['founder', 'eigenaar', 'oprichter', 'cto', 'cfo', 'ceo', 'co-founder', 'cso', 'entrepreneur', 'co-owner', 'owner', 'building', 'build', 'builder', 'residence', 'stealth', 'working'])
        
        return False if bad_keyword_found else good_keyword_found
    
    def get_report_table(self):
        # we want to know the total report of this scraper, so we must sum over the columns
        # problem is... the first column is type string, so therefore the entire array is type string
        # delete first column (which is string) and convert the rest to integers
        
        # turn report into numpy array and delete the first 'string' column, and take the sums
        report_table = self.reports.copy()
        table = np.array(report_table)
        int_table = np.delete(table, [0], axis=1).astype(int)
        sums = np.sum(int_table, axis=0)
        
        # create new row for total scores and add the column sums
        total_row = ['TOTAL']
        total_row.extend(sums)

        # add a row that indicates a seperation and then the TOTAL row
        report_table.append(['--- +','--- +', '--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +','--- +'])
        report_table.append(total_row)

        return report_table
    
    def get_report(self):
        # create a string with the report and return
        s = f"Scraper Report for Page: {self.uni}\n\n"
        s += tabulate(self.get_report_table(), headers=['Keyword', 'Start Year', 'End Year', 'Count on page', 'Profiles found', 'New', 'New title', 'Old', 'Error', 'Outside connection range', 'Scrolls'], tablefmt='orgtbl')
        return s

class BigUNIPage (UNIPage):
    def __init__(self, driver: Remote, pre_seed, url, name) -> None:
        super().__init__(driver, pre_seed, url, name)
    
    # since there are many profiles, we must filter them to make sure we find the correct profiles
    # 1st: we filter on titles that often correspond with founders
    # 2nd: we filter on start and end year to find segments that do not result in more than 1000 results (since that is the limit that linkedin shows on the page)
    def create_urls(self, use_filters=True):
        titles = ['founder', 'cto', 'cfo', 'ceo', 'oprichter', 'eigenaar', 'cso', 'co-founder', 'entrepreneur', 'chief', 'officer', 'builder', 'building']
        titles = ['founder', 'cto', 'ceo']
        base_url = self.url if self.url[-1] == '/' else self.url + '/'
        
        year_segments = [1980, 1985, 1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
        urls = []
        for t in titles:
            for i in range(len(year_segments)-1):
                urls.append(base_url + f"?educationEndYear={year_segments[i+1]}&educationStartYear={year_segments[i]}&keywords={t}")

        return urls