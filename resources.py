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
    ProfilePicture = Selector(By.XPATH, '//*[contains(@class, "render-mode-BIGPIPE")]')

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
    def __init__(self, name, url, big=False) -> None:
        self.name = name
        self.url = url
        self.big = big
    