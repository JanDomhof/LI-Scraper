from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class Selector:
    """class to create objects for selecting or targetting a certain element
        on the page

        Args:
            ST (str): Selector Type: ie XPATH or CSSSelector
            SP (str): Path of the element according to selector type
    """
    ST: str
    SP: str


class LoginPageResources:
    URL = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
    UsernameField = Selector(By.XPATH, '//input[@id="username"]')
    PasswordField = Selector(By.XPATH, '//input[@id="password"]')
    LoginButton = Selector(By.XPATH, '//button[@aria-label="Sign in"]')

class UniPageResources:
    FunctionField = Selector(By.XPATH, '//*[@id="people-search-keywords"]')
    StartYearField = Selector(By.XPATH, '//*[@id="people-search-year-start"]')
    EndYearField = Selector(By.XPATH, '//*[@id="people-search-year-end"]')
    ShowMoreButton = Selector(By.XPATH, '//*[contains(@class, "scaffold-finite-scroll__load-button")]')
    Founder = Selector(By.XPATH, '//*[contains(@class, "org-people-profile-card__profile-info")]')
    FounderName = Selector(By.XPATH, './/*[contains(@class, "artdeco-entity-lockup__title")]/a/div')
    FounderTitle = Selector(By.XPATH, './/*[contains(@class, "artdeco-entity-lockup__subtitle")]/div/div')
    FounderLink = Selector(By.XPATH, './/*[contains(@class, "app-aware-link")]')
    RemoveFilterButton = Selector(By.XPATH, '//button[contains(@aria-label, "Remove")]')
    MemberCountField = Selector(By.XPATH, './/h2[@class="text-heading-xlarge"]')

class TUDelftResources (UniPageResources):
    URL = "https://www.linkedin.com/school/tudelft/people/"


class EURResources (UniPageResources):
    URL = "https://www.linkedin.com/school/erasmus-university-rotterdam/people/"

class UNI:
    def __init__(self, name, url, year_option=True) -> None:
        self.name = name
        self.url = url
        self.year_option = year_option

        self.seed_runtime = 0
        self.seed_total = 0
        self.seed_new = 0
        self.seed_new_title = 0
        self.seed_old = 0
        self.seed_error = 0

        self.pre_seed_runtime = 0
        self.pre_seed_total = 0
        self.pre_seed_new = 0
        self.pre_seed_new_title = 0
        self.pre_seed_old = 0
        self.pre_seed_error = 0


    def set_seed_report(self, runtime, total, new, new_title, old, error) -> None:
        self.seed_runtime = runtime
        self.seed_total = total
        self.seed_new = new
        self.seed_new_title = new_title
        self.seed_old = old
        self.seed_error = error

    def set_pre_seed_report(self, runtime, total, new, new_title, old, error) -> None:
        self.pre_seed_runtime = runtime
        self.pre_seed_total = total
        self.pre_seed_new = new
        self.pre_seed_new_title = new_title
        self.pre_seed_old = old
        self.pre_seed_error = error

    def get_report(self) -> str:
        return f"""
=========================
University Scraper Report
University name: {self.name}
University url: {self.url}

SEED REPORT
Found a total of {self.seed_total} profiles in {self.seed_runtime} minutes:
Nr of new profiles: {self.seed_new}
Nr of profiles with a new title: {self.seed_new_title}
Nr of already known profiles: {self.seed_old}
Nr of errors: {self.seed_error}

PRE SEED REPORT
Found a total of {self.pre_seed_total} profiles in {self.pre_seed_runtime} minutes:
Nr of new profiles: {self.pre_seed_new}
Nr of profiles with a new title: {self.pre_seed_new_title}
Nr of already known profiles: {self.pre_seed_old}
Nr of errors: {self.pre_seed_error}
=========================
"""
    
    