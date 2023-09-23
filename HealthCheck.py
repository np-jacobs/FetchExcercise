from collections import defaultdict
import sys
import yaml
import requests
import time


def FindOutput(request):
    """
    This method tests if the outcome of an HTTP request is "UP" or "DOWN". 
    It is "UP" if the HTTP response code is between 200-299 and the response 
    latency is less than 500ms. It is "DOWN" if either conditions for "UP" 
    aren't met.

    :parameter request: An HTTP request 
    :return: "UP" if the conditions stated above are met, and "DOWN" otherwise
    """
    if ((request.__dict__["status_code"] < 200 or request.__dict__["status_code"] > 299) or
            request.elapsed.total_seconds() >= 0.5):
        return "DOWN"
    else:
        return "UP"

def TestEndpoint(endpoint: dict):
    """
    Given a dictionary representing an HTTP endpoint, this method makes an HTTP request 
    and determines its outcome.

    :parameter endpoint: A dictionary representation of an HTTP endpoint, including at 
                         least a "url" key
    :return: "UP" if the given endpoint's request had an outcome of "UP" and "DOWN" otherwise
    """
    method = "GET"  # initialize method
    r = None # initialize request tracker
    
    # check if method value is included
    if "method" in endpoint:
        method = endpoint["method"]

    if method == "GET":
        r = requests.get(endpoint["url"], headers = endpoint.get("headers"))
    elif method == "POST":
        r = requests.post(endpoint["url"], endpoint.get("body"), headers=endpoint.get("headers"))
    elif method == "PUT":
        r = requests.put(endpoint["url"], endpoint.get("body"), headers=endpoint.get("headers"))
    return FindOutput(r) # determine if the request is UP or DOWN

def HealthCheck(file: str):
    """
    This method parses a file in YAML format and loops through its endpoints, 
    calculating each domain's availability percentage every 15 seconds and displaying them
    in the console. Pressing CTRL+c ends the loop.

    :parameter file: The path to the YAML formatted file in string form 
    """
    # open and parse the file using PyYAML (converts to dictionary)
    with open(file, 'r') as file:
        data = yaml.safe_load(file)
    domains = dict() # the dictionary for logging the ongoing results
    testcounter = 1
    print ("\nWelcome! Press CTRL+c to quit the program.\n")
    try:
        while True:
            # search through the dictionary of HTTP endpoints
            for endpoint in data:
                # grab domain name from "name" entry and check if in dict
                domain = endpoint["name"].split(" ")[0]
                if domain not in domains:
                    # initialize dict with the domain and a list of zeros
                    domains[domain] = [0, 0]

                # check the method of the endpoint
                out = TestEndpoint(endpoint)

                # check the endpoint's method
                if out == "UP":
                    domains[domain][0] += 1
                elif out == "DOWN":
                    domains[domain][1] += 1

            # calculate availability % for each url domain and log to console
            print("TEST LOOP %s:" % testcounter)
            for d in domains:
                avail = 100 * (domains[d][0] / (domains[d][0] + domains[d][1]))
                # round the percentage and make it into a string
                avail = str(round(avail))
                print(d + " has " + avail + "% availability percentage")
            print("\n")
            time.sleep(1)  # start the next test cycle in 15s
            testcounter += 1
    except KeyboardInterrupt:
        print("Exiting program")

def main():
    HealthCheck(sys.argv[1])

if __name__ == "__main__":
    main()
