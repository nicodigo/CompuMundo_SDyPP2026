#Constant Integration Constant Destruction

import requests

def get_status_code(url):
    response = requests.get(url = url)
    return response.status_code

st_code = get_status_code("https://www.unlu.edu.ar")
print(st_code)
