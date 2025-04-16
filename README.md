# Fetch Rewards SRE take-home excercise

My fork of the completed Site Reliability Engineer take-home assessment. I will be detailing how to install and run the script and what changes I made.

## How to install

Open your terminal, navigate to your desired direcotry, and run the following command:

```
git clone https://github.com/youssef-qteishat/sre-take-home-exercise-python.git
```

## How to run the script

Navigate to the project direcotry, and run main.py with the config yaml file as a paramater, as such:

```
python main.py <config_file_path>
```

Afterwards, the cumulative availability of all endpoints will be evaluated and logged in terminal every 15 seconds. And to stop the script, type **Ctrl+C**. Feel free to change the ```config.yaml``` file to your liking as well, just make sure to follow the same configuration as the ```sample.yaml```.

## Changes

### monitor_endpoints(file_path):

Beforehand, the domain was returned by spliting the url string at ```//```, then spliting it again at ```/```. However, this would not exclude the port number that comes directly after the port name (Ex: example.com:800). 

In order to isolate the domain name, I utilized the ```urlparse(url)``` function ```urllib.parse``` module to parse the url into multiple components, then I returned the hostname as ```urlparse(url).hostname```.

### check_health(endpoints):

Each endpoint in the config file has certain fields specfied (name, body, method, etc). If the method field is not specficed, then it defaults to **GET**. In addition, the body field's value is a string, but the request function expects a json value. To fix this, the string is converted into a ditionary if the value is not null.

The script is expected to determine availability based on two conditions, if the response status is within the 200 to 299 range and the response time is at most 15ms. the starter code accounted for the first condition but not the second. To fix this, the time was taken before and after the request was made and both conditions where checked.

