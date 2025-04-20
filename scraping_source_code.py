import requests
import json
import multiprocessing

# Replace with your Etherscan API key
API_KEY = ''

# Etherscan API URL
API_URL = "https://api.etherscan.io/api"

# Function to get contract source code
def get_contract_source(address):
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address.split('_')[0],
        "apikey": API_KEY
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if data["status"] == "1":
        return address, data["result"][0]["SourceCode"]
    else:
        return address, None

def fetch_contract_sources_concurrently(contract_addresses):
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(get_contract_source, contract_addresses)
    return results

def main():
    with open('vulnerabilities.json', 'r') as f:
        vulnerabilities = json.load(f)
    
    contract_addresses = [entry for entry in vulnerabilities]

    contract_sources = fetch_contract_sources_concurrently(contract_addresses)

    with open('contract_sources.json', 'w') as f:
        json.dump(contract_sources, f, indent=4)

    print("Finished fetching contract sources and saved results.")

# Run the main function
if __name__ == "__main__":
    main()
