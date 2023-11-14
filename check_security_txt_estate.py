import requests
import re
from datetime import datetime
from termcolor import colored

def check_security_txt(urls):
    for url in urls:
        try:
            # Normalize the URL to ensure it ends with .well-known/security.txt
            if not url.endswith('.well-known/security.txt'):
                if not url.endswith('/'):
                    url += '/'
                url += '.well-known/security.txt'
            
            response = requests.get(url)

            # If the security.txt file exists
            if response.status_code == 200:
                content = response.text
                # Regular expression to find the Expires field
                match = re.search(r'^Expires: (.+)$', content, re.MULTILINE | re.IGNORECASE)

                if match:
                    expires_str = match.group(1).strip()
                    # Parse the Expires timestamp considering the 'Z' for UTC time
                    expires_date = datetime.strptime(expires_str, "%Y-%m-%dT%H:%M:%SZ")
                    current_date = datetime.utcnow()

                    # Check if the current date is before the expiration date
                    if current_date < expires_date:
                        print(colored(f'[OK] {url} - Expires: {expires_str}', 'green'))
                    else:
                        print(colored(f'EXPIRED {url} - Expires: {expires_str}', 'red'))
                else:
                    print(colored(f'[UNKNOWN] {url} - No Expires field found','magenta'))
            else:
                print(colored(f'[MISSING] {url} - security.txt not found', 'yellow'))
        except Exception as e:
            print(f'[ERROR] Could not process {url}: {e}')


# List of base URLs to check
urls = [
    'https://www.emburse.com',
    'https://chromeriver.com',
    'https://www.captio.net',
    'https://tripbam.rocks',    
    'https://nexonia.com',
    'https://getroadmap.com',
    'https://www.abacus.com/',
    'https://spend.emburse.com'


    # Add more URLs here
]

check_security_txt(urls)
