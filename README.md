# FetchExcercise
This program is designed to take a YAML file of HTTP endpoints as its input and test their health every 15 seconds, logging each domain's cumulative availability percentage.
## Running the Program
To run this program, install the dependencies (instructions listed below) and run `python HealthCheck.py <path/>to/.yml/file>`, with the path to the file of endpoints relative to your working directory in between the angle brackets. There is a sample of a well-formed YAML configuration file included.
## Installing Dependencies Instructions:
This program makes use of the PyYAML and Requests libraries for Python. There is a requirements.txt file provided for installing these dependencies.

Open either Terminal on Mac or PowerShell on Windows and type this command to install the modules into your project environment:
`pip install -r requirements.txt`