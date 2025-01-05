import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Retrieve credentials
STUDENT_ID = os.getenv("STUDENT_ID")
STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD")

if not STUDENT_ID or not STUDENT_PASSWORD:
    raise EnvironmentError("Environment variables STUDENT_ID and STUDENT_PASSWORD are required in the .env file.")

# Path to Brave Browser
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

# Path to Chromedriver
chromedriver_path = "C:/chromedriver-win64/chromedriver.exe"

# Configure Brave options
# Configure Brave options
options = Options()
options.binary_location = brave_path
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")


# Set up WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Step 1: Log in using Selenium
    driver.get("https://al-zahraa.mans.edu.eg/studentLogin")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))
    driver.find_element(By.NAME, "txtStudentID").send_keys(STUDENT_ID)
    driver.find_element(By.NAME, "txtStudentPassword").send_keys(STUDENT_PASSWORD)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "account-btn"))
    )
    login_button.click()

    # Step 2: Navigate to the submenu and click "getMeals"
    sidebar_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sidebar-menu"))
    )
    second_submenu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='sidebar-menu']//li[@class='submenu'][2]"))
    )
    second_submenu.click()
    get_meals_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='sidebar-menu']//li[@class='submenu'][2]//a[@id='getMeals']"))
    )
    get_meals_button.click()
    # Introduce a short delay
    time.sleep(2)
    # Step 3: Extract cookies from Selenium
    cookies = driver.get_cookies()
    session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}

    # Step 4: Prepare the POST request
    url = "https://al-zahraa.mans.edu.eg/studentHome"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "al-zahraa.mans.edu.eg",
        "Origin": "https://al-zahraa.mans.edu.eg",
        "Referer": "https://al-zahraa.mans.edu.eg/studentHome",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    # Step 5: Define the payload
    payload = {
        "fnName": "bookMeals",
        "chkMeals": "7/1/2025|20.7746."
    }

    # Step 6: Send the POST request
    response = requests.post(url, headers=headers, cookies=session_cookies, data=payload)
    print("cookies:", session_cookies)
    print("payload:", payload)
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.content.decode('utf-8'))

    print("Response Text:", response.text)

finally:
    # Close the browser
    driver.quit()
