from config import Config
from modules.automation import BookingAutomation
from modules.api_client import APIClient
from modules.date import TomorrowDate
from modules.messaging import MessagingService
from modules.file_encryption import FileEncryption
import json
import os
import traceback
import time


class BookingScript:
    def __init__(self):
        """Initialize the BookingScript class."""
        self.config = None
        self.messaging = None
        self.automation = None
        self.initialize_services()

    def initialize_services(self):
        """Initialize configuration, messaging, and automation services."""
        try:
            Config.validate()
            self.messaging = MessagingService(
                whatsapp_app_url=Config.WHATSAPP_APP_URL,
                whatsapp_app_key=Config.WHATSAPP_APP_KEY,
                whatsapp_app_secret=Config.WHATSAPP_APP_SECRET,
            )
            self.automation = BookingAutomation(Config.BRAVE_PATH, Config.CHROMEDRIVER_PATH)
        except Exception as init_exception:
            error_message = f"Failed to initialize services: {str(init_exception)}"
            traceback_details = traceback.format_exc()
            self.send_error_notification(error_message, traceback_details)
            raise

    def send_error_notification(self, notification_error_message, notification_traceback):
        """Send error notifications."""
        try:
            self.messaging.notify_failure(Config.WHATSAPP_NUMBER, notification_error_message)
            self.messaging.notify_failure(Config.WHATSAPP_NUMBER, notification_traceback)
        except Exception as notify_exception:
            print(f"Failed to send error notification: {str(notify_exception)}")

    def execute(self):
        decrypted_file = None  # Initialize with None to avoid reference before assignment
        """Main execution flow of the script."""
        try:
            # Decrypt the user file
            encryptor = FileEncryption()
            encrypted_file = Config.ENCRYPTED_FILE_PATH
            decrypted_file = Config.DECRYPTED_FILE_PATH
            encryptor.decrypt_file(encrypted_file, decrypted_file)

            with open(decrypted_file, "r") as file:
                users = json.load(file)

            # Process each user
            for user in users:
                try:
                    student_id = user["student_id"]
                    student_password = user["password"]
                    meal_type = user["mealType"]

                    self.automation.clear_cache()
                    self.automation.login(Config.LOGIN_URL, student_id, student_password)
                    self.automation.open_sidebar()
                    self.automation.navigate_to_meals()

                    cookies = self.automation.get_cookies()
                    headers = {
                        "Accept": "*/*",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                    }
                    tomorrow_date = TomorrowDate().get_tomorrow_date()
                    data = (
                        {"fnName": "bookMeals", "chkMeals": tomorrow_date + "|20.7746."}
                        if meal_type == "lunch"
                        else {"fnName": "bookMeals", "chkMeals": tomorrow_date + "|20.8134.,"
                                                                 + tomorrow_date + "|20.7746."}
                    )
                    response = APIClient.post_request(Config.HOME_URL, headers, cookies, data)

                    if not response.get("hasError"):
                        message = f"Meals booking successful for user {student_id}."
                        self.messaging.send_message(user["phone"], message)
                    else:
                        booking_error_message = f"Booking failed for {student_id}: {response.get('errMsg')}."
                        self.messaging.notify_failure(user["phone"], booking_error_message)
                except Exception as user_exception:
                    user_error_message = f"Error for user {user['student_id']}: {str(user_exception)}"
                    user_traceback_details = traceback.format_exc()
                    self.messaging.notify_failure(user["phone"], user_error_message)
                    self.messaging.notify_failure(user["phone"], user_traceback_details)

        except Exception as general_exception:
            general_error_message = f"General exception occurred: {str(general_exception)}"
            general_traceback_details = traceback.format_exc()
            self.send_error_notification(general_error_message, general_traceback_details)
        finally:
            if os.path.exists(decrypted_file):
                os.remove(decrypted_file)
            self.automation.close()


if __name__ == "__main__":
    max_retries = 3
    retry_delay = 300  # Time in seconds (e.g., 5 minutes)
    script = None  # Ensure script is defined before the loop

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} of {max_retries}")
            script = BookingScript()
            script.execute()
            print("Script executed successfully.")
            break  # Exit loop if successful
        except Exception as e:
            error_message = f"Attempt {attempt + 1} failed: {str(e)}"
            traceback_details = traceback.format_exc()
            print(error_message)
            if script:  # Check if script is initialized
                try:
                    script.send_error_notification(error_message, traceback_details)
                except Exception as notify_exception:
                    print(f"Failed to send notification: {str(notify_exception)}")
            else:
                print("Error notification could not be sent because 'script' is not initialized.")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting.")
