# Fetch Rewards SRE take-home exercise

My fork of the completed Site Reliability Engineer take-home assessment. I will be detailing how to install and run the script and what changes I made.

## How to install

Open your terminal, navigate to your desired directory, and run the following command:

```
git clone https://github.com/youssef-qteishat/sre-take-home-exercise-python.git
```

## How to run the script

Navigate to the project directory, and run main.py with the config yaml file as a parameter, as such:

```
python main.py <config_file_path>
```

Afterward, the cumulative availability of all endpoints will be evaluated and logged in the terminal every 15 seconds. The script can be stopped simply by typing **Ctrl+C**. Feel free to change the ```config.yaml``` file to your liking as well. Just make sure to follow the same configuration as the ```sample.yaml```.

## Changes Made

### monitor_endpoints(file_path):

Beforehand, the domain was returned by splitting the URL string at ```//```, then splitting it again at ```/```. However, this would not exclude the port number that comes directly after the port name (Ex: example.com:800). 

To isolate the domain name, I utilized the ```urlparse(url)``` function ```urllib.parse``` module to parse the URL into multiple components, then I returned the hostname as ```urlparse(url).hostname```.

### check_health(endpoints):

Each endpoint in the config file has certain fields specified (name, body, method, etc). If the method field is not specified, then it defaults to **GET**. In addition, the body field's value is a string, but the request function expects a JSON value. This is fixed by converting the string into a dictionary if the value is not null.

The script is expected to determine availability based on two conditions: If the response status is within the 200 to 299 range and the response time is at most 500ms. The starter code accounted for the first condition but not the second. This is addressed by calculating the elapsed time and checking both conditions.
