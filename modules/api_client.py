import requests

class APIClient:
    @staticmethod
    def post_request(url, headers, cookies, data):
        # print("URL:", url)
        # print("Headers:", headers)
        # print("Cookies:", cookies)
        # print("Payload:", data)
        try:
            response = requests.post(url, headers=headers, cookies=cookies, data=data)
            # print("Response Status Code:", response.status_code)
            # print("Response Body:", response.text)

            # Raise exception for non-2xx status codes
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            # print(f"Error in API Request: {e}")
            return {"hasError": True, "errMsg": str(e)}