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
    def __init__(self, driver:Remote) -> None:
        self.driver: Remote = driver
        self.driver.maximize_window()
        self.db = profiles_db()
        self.edda = Edda()

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
    
    def scrape_page(self, title):
        # Enter the 
        title_field = self.wait_until_find(TUDelftResources.FunctionField, 10)
        self.click(title_field)
        self.send_keys(title_field, title).send_keys(Keys.ENTER)

        time.sleep(5)

        start_year_field = self.wait_until_find(TUDelftResources.StartYearField, 10)
        self.click(start_year_field)
        self.send_keys(start_year_field, "2015").send_keys(Keys.ENTER)

        time.sleep(5)

        for _ in range(3):
            show_more_button = self.wait_until_find(TUDelftResources.ShowMoreButton, 10)
            self.scroll_to_element(show_more_button)
            time.sleep(1)

        self.founder_elements = self.wait_until_find_all(TUDelftResources.Founder, 10)

    def persist(self):
        self.db.insert(self.founders)

    def close(self):
        self.db.close()
    
    def scrape(self):
        titles = ["founder"]
        for title in titles:
            self.scrape_page(title)

        founder_names_db = self.db.fetch_names()
        assignees = self.db.fetch_assignees()
        self.founders = []

        for founder in self.founder_elements:
            if self.find_from_element(founder, TUDelftResources.FounderName).text.strip() not in founder_names_db:
                edda_response = self.edda.get_company_by_name(self.find_from_element(founder, TUDelftResources.FounderName).text.strip())
                in_edda = 1 if len(edda_response) > 0 else 0
                edda_company = self.edda.get_company_by_id(edda_response["id"]) if in_edda else None
                self.founders.append({
                    "Name": self.find_from_element(founder, TUDelftResources.FounderName).text.strip(),
                    "Linkedin": self.find_from_element(founder, TUDelftResources.FounderLink).get_attribute("href"),
                    "Title": self.find_from_element(founder, TUDelftResources.FounderTitle).text.strip(),
                    "University": self.uni,
                    "Year": None,
                    "TitleIndicatesFounder": 1 if any(
                        keyword in self.find_from_element(founder, TUDelftResources.FounderTitle).text.lower().strip() for keyword in
                        ['founder', 'eigenaar', 'oprichter', 'cto', 'cfo', 'ceo']) else 0,
                    "InEdda": 1 if in_edda else 0,
                    "MatchingEddaWord": edda_response[0]["name"] if in_edda else "",
                    "Assignee": edda_company["owners"][0]["firstname"] if in_edda else min(assignees, key=assignees.get),
                    "Checked": 0,
                    "AddedToEdda": 0,
                    "Vertical": self.edda.get_company_fields("864", edda_response["id"])["value"]["name"] if in_edda else None
                })
                print(self.founders[-1])
                assignees[min(assignees, key=assignees.get)] += 1
                break

class LoginPage (BasePage):
    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        self.url = LoginPageResources.URL

    def login(self, email: str, password: str):       
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
    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        self.url = TUDelftResources.URL
        self.uni = "TU Delft"

class EURPage (BasePage):
    def __init__(self, driver: Remote) -> None:
        super().__init__(driver)
        self.url = EURResources.URL
        self.uni = "Erasmus University Rotterdam"
