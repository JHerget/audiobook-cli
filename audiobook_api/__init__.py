from .client import AudiobookApi

def login(username: str, password: str):
    client = AudiobookApi()
    response = client.login(username, password)
    
    if not response.ok:
        print("Login unsuccessful.")
        quit()

    return client

__all__ = ["AudiobookApi", "login"]
