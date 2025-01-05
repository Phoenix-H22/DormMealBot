from config import Config
from automation import BookingAutomation
from api_client import APIClient
from date import TomorrowDate
from messaging import MessagingService
from file_encryption import FileEncryption
import json
import os

def main():
    # Validate configuration
    Config.validate()

    # Initialize services
    automation = BookingAutomation(Config.BRAVE_PATH, Config.CHROMEDRIVER_PATH)
    messaging = MessagingService(
        whatsapp_app_url=Config.WHATSAPP_APP_URL,
        whatsapp_app_key=Config.WHATSAPP_APP_KEY,
        whatsapp_app_secret=Config.WHATSAPP_APP_SECRET,
    )
    encryptor = FileEncryption()  # To handle user file decryption

    # Define file paths
    encrypted_file = "users.json.enc"
    decrypted_file = "users_decrypted.json"

    try:
        # Decrypt the users.json.enc file
        encryptor.decrypt_file(encrypted_file, decrypted_file)

        # Load users from the decrypted file
        with open(decrypted_file, "r") as file:
            users = json.load(file)

        # Iterate over users to book meals
        for user in users:
            try:
                student_id = user["student_id"]
                student_password = user["password"]

                # Clear browser cache before login
                automation.clear_cache()

                # Login and navigate
                automation.login("https://al-zahraa.mans.edu.eg/studentLogin", student_id, student_password)
                automation.navigate_to_meals()

                # Get cookies
                cookies = automation.get_cookies()

                # Send API request for booking meals
                url = "https://al-zahraa.mans.edu.eg/studentHome"
                headers = {
                    "Accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                }
                tomorrow_date = TomorrowDate().get_tomorrow_date()
                data = {"fnName": "bookMeals", "chkMeals": tomorrow_date + "|20.7746."}
                response = APIClient.post_request(url, headers, cookies, data)

                # Verify booking and send WhatsApp message
                if not response.get("hasError"):
                    message = f"Meals booking successful for user {student_id}."
                    messaging.send_message(user["phone"], message)
                else:
                    error_message = f"Booking failed for {student_id}: {response.get('errMsg')}."
                    print(error_message)
                    messaging.notify_failure(user["phone"], error_message)

            except Exception as e:
                error_message = f"Error for user {user['student_id']}: {str(e)}"
                print(error_message)
                messaging.notify_failure(user["phone"], error_message)

    except Exception as e:
        # Notify on any unhandled exceptions
        error_message = f"Unhandled Exception: {str(e)}"
        print(error_message)
        messaging.notify_failure(Config.WHATSAPP_APP_URL, error_message)

    finally:
        if os.path.exists(decrypted_file):
            os.remove(decrypted_file)
            print("Temporary decrypted file removed.")
        automation.close()

if __name__ == "__main__":
    main()
