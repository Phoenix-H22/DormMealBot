from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "C:/chromedriver-win64/chromedriver.exe")
    BRAVE_PATH = os.getenv("BRAVE_PATH", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
    # Existing variables
    WHATSAPP_APP_URL = os.getenv("WHATSAPP_APP_URL")
    WHATSAPP_APP_KEY = os.getenv("WHATSAPP_APP_KEY")
    WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    @staticmethod
    def validate():
        """Validate that all required environment variables are set."""
        if not Config.ENCRYPTION_KEY:
            raise EnvironmentError("ENCRYPTION_KEY must be set in the .env file.")
