import requests

class MessagingService:
    def __init__(self, whatsapp_app_url, whatsapp_app_key, whatsapp_app_secret):
        self.app_url = whatsapp_app_url
        self.app_key = whatsapp_app_key
        self.app_secret = whatsapp_app_secret

    def send_message(self, to, message, sandbox="false"):
        payload = {
            "appkey": self.app_key,
            "authkey": self.app_secret,
            "to": to,
            "message": message,
            "sandbox": sandbox,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(self.app_url, data=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending WhatsApp message: {e}")
            return None

    def notify_failure(self, to, error_message):
        failure_message = f"Script failed with error:\n{error_message}"
        print(f"Sending failure notification: {failure_message}")
        return self.send_message(to, failure_message)
