import requests

def collect_emails():
    api_key = 'de63cd672351c62c592188b09511d4c24b811f16'
    
    domain = 'marrlabs.com'
    first_name = 'Dave'
    last_name = 'Grannan'

    # Construct the URL for the API request
    url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={api_key}"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()
        # Do something with the data, for example, print it
        print(data)
    else:
        print(f"Failed to get data, status code: {response.status_code}")