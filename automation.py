from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
class BookingAutomation:
    def __init__(self, brave_path, chromedriver_path):
        options = webdriver.ChromeOptions()
        options.binary_location = brave_path
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

    def clear_cache(self):
        """Clear browser cache to save storage and ensure fresh sessions."""
        self.driver.get("chrome://settings/clearBrowserData")
        ActionChains(self.driver).send_keys(Keys.TAB * 4 + Keys.ENTER).perform()
        print("Browser cache cleared.")
        self.driver.implicitly_wait(5)  # Wait for the cache-clearing process
    def login(self, url, student_id, password):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))
        self.driver.find_element(By.NAME, "txtStudentID").send_keys(student_id)
        self.driver.find_element(By.NAME, "txtStudentPassword").send_keys(password)
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "account-btn"))
        )
        login_button.click()

    def navigate_to_meals(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "sidebar-menu"))
        )
        submenu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='sidebar-menu']//li[@class='submenu'][2]"))
        )
        submenu.click()
        get_meals_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='sidebar-menu']//li[@class='submenu'][2]//a[@id='getMeals']"))
        )
        get_meals_button.click()

    def get_cookies(self):
        return {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}

    def close(self):
        self.driver.quit()
