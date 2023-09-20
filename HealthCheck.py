from collections import defaultdict
import yaml
import requests
import time

#* 5.) Add commenting
#* 10.) Write instructions for yaml and requests
"""


"""
def FindOutput(request):
    if ((request.__dict__["status_code"] < 200 or request.__dict__["status_code"] > 299) or 
        request.elapsed.total_seconds() >= 0.5):
        return "DOWN"
    else: 
        return "UP"
    
def TestEndpoint(endpoint: dict):
    method = "GET" # initialize method
    
    # check if method value is included
    if "method" in endpoint:
        method = endpoint["method"]
    
    if method == "GET":
        # if headers are included, make the request including them
        if "headers" in endpoint:
            r = requests.get(endpoint["url"], endpoint["headers"])
            return FindOutput(r)  # determine the outcome of the request (UP or DOWN)
        # otherwise, make the request without headers
        else:
            r = requests.get(endpoint["url"])
            return FindOutput(r)
    elif method == "POST":
        # if body and headers included, make the request with those parameters 
        if "body" in endpoint and "headers" in endpoint:
            r = requests.post(endpoint["url"], endpoint["body"], headers=endpoint["headers"])
            return FindOutput(r)
        # if just the body is included
        elif "body" in endpoint:
            r = requests.post(endpoint["url"], endpoint["body"])
            return FindOutput(r)
    elif method == "PUT":
        # if body and headers included, make the request with those parameters 
        if "body" in endpoint and "headers" in endpoint:
            r = requests.put(endpoint["url"], endpoint["body"], headers=endpoint["headers"])
            return FindOutput(r)
        # only body included
        elif "body" in endpoint:
            r = requests.put(endpoint["url"], endpoint["body"])
            return FindOutput(r)
        # only headers included
        elif "headers" in endpoint:
            r = requests.put(endpoint["url"], headers=endpoint["headers"])
            return FindOutput(r)
        # body and headers aren't included
        else:
            r = requests.put(endpoint["url"])
            return FindOutput(r)

def HealthCheck(file: str):
    # open and parse the file using PyYAML (converts to dictionary)
    with open(file, 'r') as file:
        data = yaml.safe_load(file)
    domains = dict()
    testcounter = 1
    try: 
        while True:
            # search through the dictionary of HTTP endpoints 
            for endpoint in data:
                # grab domain name from "name" entry and check if in dict
                domain = endpoint["name"].split(" ")[0] 
                if domain not in domains:
                    domains[domain] = [0,0] # initialize dict with the domain and a list of zeros 
                
                out = TestEndpoint(endpoint) # check the method of the endpoint
                
                # check the endpoint's method
                if out == "UP":
                    domains[domain][0] += 1
                elif out == "DOWN":
                    domains[domain][1] += 1

            # calculate availability % for each url domain and log to console 
            print("TEST LOOP %s:" % testcounter)
            for d in domains:
                avail = 100 * (domains[d][0] / (domains[d][0] + domains[d][1]))
                avail = str(round(avail)) # round the percentage and make it into a string
                print(d + " has " + avail + "% availability percentage") 
            print("\n") 
            time.sleep(1) # start the next test cycle in 15s
            testcounter +=1    
    except KeyboardInterrupt:
        print("Exiting program")
def main():
    HealthCheck("SampleInput.yml")

if __name__ == "__main__":
    main()

