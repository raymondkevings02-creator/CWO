import requests

def test_api_endpoints():
    base_url = 'http://localhost:5000'  # Use HTTP instead of HTTPS for testing
    endpoints = ['/api/conducteurs', '/api/investisseurs']

    for endpoint in endpoints:
        try:
            response = requests.get(base_url + endpoint, verify=False)
            print(f"Endpoint {endpoint}: Status {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data received: {len(data)} items")
                if data:
                    print(f"Sample item: {data[0]}")
            else:
                print(f"Failed to fetch data: {response.text}")
        except Exception as e:
            print(f"Error testing {endpoint}: {str(e)}")

if __name__ == '__main__':
    test_api_endpoints()
