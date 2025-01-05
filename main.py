import json
import os

from config import Config
from automation import BookingAutomation
from api_client import APIClient
from date import TomorrowDate
from messaging import MessagingService

def main():
    Config.validate()

    # Initialize services
    automation = BookingAutomation(Config.BRAVE_PATH, Config.CHROMEDRIVER_PATH)
    messaging = MessagingService(
        whatsapp_app_url=Config.WHATSAPP_APP_URL,
        whatsapp_app_key=Config.WHATSAPP_APP_KEY,
        whatsapp_app_secret=Config.WHATSAPP_APP_SECRET,
    )

    try:
        # Login and navigate
        automation.login("https://al-zahraa.mans.edu.eg/studentLogin", Config.STUDENT_ID, Config.STUDENT_PASSWORD)
        automation.navigate_to_meals()

        # Get cookies
        cookies = automation.get_cookies()

        # Send API request
        url = "https://al-zahraa.mans.edu.eg/studentHome"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        tomorrow_date = TomorrowDate().get_tomorrow_date()
        # tomorrow_date = "7/1/2025"
        data = {"fnName": "bookMeals", "chkMeals": tomorrow_date +"|20.7746."}
        response = APIClient.post_request(url, headers, cookies, data)

        # Verify booking and send WhatsApp message
        if not response.get("hasError"):
            messaging.send_message(Config.WHATSAPP_NUMBER, "Meals booking was successful.")
        else:
            error_message = f"Booking failed: {response.get('errMsg')}"
            print(error_message)
            messaging.notify_failure(Config.WHATSAPP_NUMBER, error_message)

    except Exception as e:
        # Notify on any unhandled exceptions
        error_message = str(e)
        print(f"Unhandled Exception: {error_message}")
        messaging.notify_failure(Config.WHATSAPP_NUMBER, error_message)

    finally:
        automation.close()

if __name__ == "__main__":
    main()
