from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    STUDENT_ID = os.getenv("STUDENT_ID")
    STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD")
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "C:/chromedriver-win64/chromedriver.exe")
    BRAVE_PATH = os.getenv("BRAVE_PATH", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
    # Existing variables
    WHATSAPP_APP_URL = os.getenv("WHATSAPP_APP_URL")
    WHATSAPP_APP_KEY = os.getenv("WHATSAPP_APP_KEY")
    WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET")
    WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
    @staticmethod
    def validate():
        if not Config.STUDENT_ID or not Config.STUDENT_PASSWORD:
            raise EnvironmentError("STUDENT_ID and STUDENT_PASSWORD must be set in the .env file.")
