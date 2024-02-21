from asyncio.windows_events import NULL
from msilib.schema import AppId
import requests
import json
from requests.auth import HTTPBasicAuth

publicID = "SBOMGeneration"
# This is a function which takes the public ID of the application as input and gives us the appID. The internal appID we should use for retrieval of SBOM in further calls. 
def getApplicationID():
  url = "http://sjcvl-nexus01.cadence.com:8070/api/v2/applications?publicId="+publicID
  # TODO -- Delete the hardcoded passwords and write code to take the input from the user
  myResponse = requests.get(url, auth=HTTPBasicAuth('8jc9MjoL', 'EPC0i0NxBJOXx4MYiDjckrn5hgAtzL4bsBNcFOsrHMNp'), verify=True)
  json_data = json.loads(myResponse.text)
  #json_data = myResponse.json
  print(json_data)
  list = json_data.get('applications')
  applicationID = list[0].get('id')
  print(applicationID)
  return applicationID

# This function gives us the report ID from where we form the SBOM generation API URL and get the SBOMs of any particular application. 
def getReportID(): 
  appID = getApplicationID()
  #url = "http://sjcvl-nexus01.cadence.com:8070/api/v2/reports/applications/c189016df2f84039861a6d37a86a11d5"
  url = "http://sjcvl-nexus01.cadence.com:8070/api/v2/reports/applications/"+appID
  # TODO -- Delete the hardcoded passwords and write code to take the input from the user
  #myResponse = requests.get(url,auth=HTTPBasicAuth(input("username: "), input("Password: ")), verify=True)
  myResponse = requests.get(url,auth=HTTPBasicAuth('8jc9MjoL', 'EPC0i0NxBJOXx4MYiDjckrn5hgAtzL4bsBNcFOsrHMNp'), verify=True)
  json_data = json.loads(myResponse.text)
  var = json_data[0]
  reportIDRaw = var.get('reportHtmlUrl')
  #var = myResponse.text.rfind("report/", [0, start[0, END]] )
  reportID = reportIDRaw.split('/')[-1]
  print(reportID)
  return reportID

appID = getApplicationID()
reportID = getReportID()
# API URL for Nexus IQ Server
url = "http://sjcvl-nexus01.cadence.com:8070/api/v2/cycloneDx/1.4/"+appID+"/reports/"+reportID

# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
myResponse = requests.get(url,auth=HTTPBasicAuth('8jc9MjoL', 'EPC0i0NxBJOXx4MYiDjckrn5hgAtzL4bsBNcFOsrHMNp'), verify=True)
print (myResponse.status_code)
f = open(publicID+"_BOM.xml", "w")
f.write(myResponse.text)
f.close




