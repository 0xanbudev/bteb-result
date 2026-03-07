import requests

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.roktodan.xyz/teams',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
}

response = requests.get('https://www.roktodan.xyz/api/teams/members', headers=headers)

if response.status_code == 200:
    data = response.json()
    status = data.get('success')
    if status:
        print("API request was successful.")
        # save log
        with open('roktodan_log.txt', 'a') as log_file:
            log_file.write(f"API request successful: 200\n")
    else:
        print(f"API returned an error: {data.get('message')}")
        # save error log 
        with open('roktodan_log.txt', 'a') as log_file:
            log_file.write(f"API error: {data.get('message')}\n")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    # save error log
    with open('roktodan_log.txt', 'a') as log_file:
        log_file.write(f"HTTP error: Status code {response.status_code}\n")
