from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from resources import Selector, LoginPageResources, TUDelftResources, EURResources
from typing import List
import contextlib, pyautogui, random, time

from db import profiles_db
from edda import Edda

class BasePage:
    """Base class for all the pages
    the subclasses will contain all the methods can be perform on a
    single page

    you can start a new instance of this class as follow

    page = BasePage(driver)
    """
    def __init__(self, driver:Remote, pre_seed) -> None:
        self.driver: Remote = driver
        self.driver.maximize_window()
        self.db = profiles_db()
        self.edda = Edda()
        self.pre_seed = pre_seed
        self.founder_elements = []

        self.report_total = 0
        self.report_new = 0
        self.report_new_title = 0
        self.report_old = 0
        self.report_error = 0

        if pre_seed:
            names = ['Daan', 'Boaz', 'Ole', 'Jan', 'Tessa', 'Elsa', 'Robin', 'Rozanne', 'Sophie']
        else:
            names = ['Ileana', 'Jasper', 'Isabelle']

        self.assignees = self.db.fetch_assignees(names)
        self.founders = []




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
        for i in range(n_iter):
            try:
                show_more_button = self.wait_until_find(TUDelftResources.ShowMoreButton, 5)
                self.scroll_to_element(show_more_button)
            except:
                print(f"Reached bottom in {i} scrolls")
                break
        try:
            self.founder_elements.extend(self.wait_until_find_all(TUDelftResources.Founder, 10))
        except:
            pass

    def persist(self):
        self.db.insert(self.founders)

    def close(self):
        self.db.close()

    def create_urls(self):
        titles = ['founder', 'cto', 'cfo', 'ceo', 'oprichter', 'eigenaar', 'cso', 'co-founder', 'entrepreneur', 'chief', 'officer']
        base_url = self.url if self.url[-1] == '/' else self.url + '/'
        urls = [base_url + f"?education{'Start' if self.pre_seed else 'End'}Year=2015&keywords={t}" for t in titles]
        return urls
    
    def scrape(self):
        urls = self.create_urls()

        for url in urls:
            self.driver.get(url)
            self.scrape_page(n_iter=5000)

            db_records = self.db.fetch_name_li_title()

            for founder in self.founder_elements:
                # get name, linkedin, title to check for duplicates
                try:
                    current_founder = self.find_from_element(founder, TUDelftResources.FounderName).text.strip()
                    current_founder_li = self.find_from_element(founder, TUDelftResources.FounderLink).get_attribute("href").split("?")[0]
                    current_founder_title = self.find_from_element(founder, TUDelftResources.FounderTitle).text.strip()
                except:
                    self.report_error += 1
                    continue
                self.report_total += 1

                # if already found in this iteration, skip
                name_already_found = current_founder in [f["Name"] for f in self.founders]
                li_already_found = current_founder_li in [f["Linkedin"] for f in self.founders]
                if name_already_found or li_already_found or current_founder == "LinkedIn Member":
                    continue
                
                # check if name is already in db
                if db_records['Name'].str.contains(current_founder).any() or db_records['Linkedin'].str.contains(current_founder_li).any():
                    # if title has changed, change title and set checked to 0
                    if not db_records.loc[db_records['Name'] == current_founder]['Title'].str.contains(current_founder_title).any():
                        self.db.update_title(current_founder, current_founder_title)
                        self.report_new_title += 1
                    else:
                        self.report_old += 1
                    continue
                
                # if not in db, try to fetch all data and create new founder
                try:
                    self.founders.append({
                        "Name": current_founder,
                        "Linkedin": current_founder_li,
                        "Title": current_founder_title,
                        "University": self.uni,
                        "Year": None,
                        "TitleIndicatesFounder": 1 if self.check_if_founder(self.find_from_element(founder, TUDelftResources.FounderTitle).text.lower().strip()) else 0,
                        "InEdda": 0,
                        "MatchingEddaWord": "",
                        "Assignee": min(self.assignees, key=self.assignees.get),
                        "Checked": 0,
                        "AddedToEdda": 0,
                        "Vertical": None
                    })
                    self.report_new += 1
                    self.assignees[min(self.assignees, key=self.assignees.get)] += 1
                except Exception as e:
                    print(e)
                    self.report_error += 1
                    continue
                
            self.founder_elements = []
            remove_filter_button = self.wait_until_find(TUDelftResources.RemoveFilterButton, 10)
            self.scroll_to_element(remove_filter_button)
            self.click(remove_filter_button)

    def check_if_founder(self, title) -> bool:
        bad_keyword_found = any(keyword in title for keyword in['consultant', 'consultancy', 'consulting', 'consult', 'consultation', 'strategy', 'strategic', 'art', 'arts', 'design', 'designer', 'studio', 'architect', 'architecture', 'law', 'lawyer'])
        good_keyword_found = any(keyword in title for keyword in['founder', 'eigenaar', 'oprichter', 'cto', 'cfo', 'ceo'])
        return False if bad_keyword_found else good_keyword_found

class LoginPage (BasePage):
    def __init__(self, driver: Remote, pre_seed) -> None:
        super().__init__(driver, pre_seed)
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

        return self

class TUPage (BasePage):
    def __init__(self, driver: Remote, pre_seed) -> None:
        super().__init__(driver, pre_seed)
        self.url = TUDelftResources.URL
        self.uni = "TU Delft"

class EURPage (BasePage):
    def __init__(self, driver: Remote, pre_seed) -> None:
        super().__init__(driver, pre_seed)
        self.url = EURResources.URL
        self.uni = "Erasmus University Rotterdam"

class UNIPage (BasePage):
    def __init__(self, driver: Remote, pre_seed, url, name) -> None:
        super().__init__(driver, pre_seed)
        self.url = url
        self.uni = name