from httpx import get

def cli():
    print(
        get('http://httpbin.org/get?arg=live de Python'
        ).json()['args']['arg']
    )