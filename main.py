import yaml
import requests
import time
import json
from urllib.parse import urlparse
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# ignores port when returning domain
def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.hostname

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper() # reformat HTTP method to uppercase and defaults to GET if no method provided
    headers = endpoint.get('headers')
    body = endpoint.get('body')
    name = endpoint.get('name')

    # if body is specified, convert string to dictionary
    if body is not None:
            body = json.loads(body)

    try:

        #calculate time it takes to make request in ms
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body)
        elapsed_time = (time.time() - start_time) * 1000

        #check evailability based on reponse status and reponse time
        if (200 <= response.status_code < 300) and (elapsed_time) <= 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            domain = get_domain(endpoint["url"])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        # Sleep to log availability every 15 seconds
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")