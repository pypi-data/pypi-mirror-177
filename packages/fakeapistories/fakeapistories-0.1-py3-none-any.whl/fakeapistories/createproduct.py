import requests

API = "https://fakestoreapi.com/products"

data =  {
                    'title': 'test product',
                    'price': 13.5,
                    'description': 'lorem ipsum set',
                    'image': 'https://i.pravatar.cc',
                    'category': 'electronic'
                }

response = requests.post(url = API, data = data)
paste_url = response.text
print(paste_url)