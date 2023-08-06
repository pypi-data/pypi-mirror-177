import requests
import json

class MakeApiCall:

    def get_data(self, api):
        response = requests.get(f"{api}")
        if response.status_code == 200:
            print("Successfully fetched the data")
            self.formatted_print(response.json())
        else:
            print(f"Hello person, there a {response.status_code} error with your request")
    
    def get_user_data(self, api, parameters):
        response = requests.get(f"{api}", params=parameters)
        if response.status_code == 200:
            print("successfully fetched the data with parameters provided")
            self.formatted_print(response.json())
        else:
            print(f"Hello person, there a {response.status_code} error with your request")

    def formatted_print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)
    
    def __init__(self, api):
        parameters = {
            "username": "rohan"
        }
        self.get_user_data(api, parameters)

if __name__ == "__main__":
    api_call = MakeApiCall("https://fakestoreapi.com/products/categories")