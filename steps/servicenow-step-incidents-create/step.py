#!/usr/bin/env python
import pysnow
from nebula_sdk import Interface, Dynamic as D

relay = Interface()

# Create client object
host = relay.get(D.servicenow.connection.host)
user = relay.get(D.servicenow.connection.user)
password = relay.get(D.servicenow.connection.password)

c = None
try:
    c = pysnow.Client(host=host, user=user, password=password)
except:
    print('ERROR: Failed to authenticate to ServiceNow. Exiting.') 
    exit(1)

# Define an incident table resource
incident = c.resource(api_path='/table/incident')

# Set the payload
new_incident = {
    'short_description': relay.get(D.shortDescription),
    'description': relay.get(D.description),
    'priority': relay.get(D.priority),
    'impact': relay.get(D.impact),
    'state': relay.get(D.state)
}

# Create a new incident record
result = incident.create(payload=new_incident)

# Print the result
r = result.all()[0]
print('')
print("Created the following ServiceNow incident:\n")
print("NUMBER: ", r['number'])
print("SHORT DESCRIPTION: ", r['short_description'])
print("DESCRIPTION: ", r['description'])
print("IMPACT: ", r['impact'])
print("STATE: ", r['state'])
print("PRIORITY: ", r['priority'])

# Set the output
print('\nSetting incident details to the output `incident`')
relay.outputs.set('incident', r)
