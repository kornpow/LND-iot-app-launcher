from balena import Balena
from balena.exceptions import RequestError, ServiceNotFound
from pprint import pprint
import sys
import os

import requests


balena = Balena()

block_partition_uuid = "enter_uuid_here"

env_var_defaults = [
    ("ACTIVE_CHAIN","BITCOIN"),
    ("BITCOIND_VERSION","0.17.1"),
    ("LITECOIND_VERSION","0.16.3"),
    ("LND_VERSION","v0.7.1-beta"),
    ("BLOCKCHAIN_UUID",block_partition_uuid),
    ("BLOCKCHAIN_FSTYPE","ext4"),
]

def selectAppFromList():
	apps = balena.models.application.get_all()
	# Print all application names, and allow selection
	print("List of Indexes To Select Target Application: ")
	for i in range(0,len(apps)):
		print("{}: {}".format(i,apps[i]['app_name']))

	selection = int(input("Enter Index:  "))
	target_app = apps[selection]
	print("\n\n")

	target_details = balena.models.application.get_by_id(target_app['id'])
	pprint(target_details)
	return target_app['id']

def createDefaultBalenaENVVars(id):
    for var in env_var_defaults:
        try:
            balena.models.environment_variables.service_environment_variable.create(id, 'main', var[0], var[1])
            print("SUCCESS: Created Variable %s with Value: %s" % (var[0],var[1]) )
        except ServiceNotFound as e:
            print("ERROR: You must have pushed to the balena origin at least once to create environment variables! Service Name: %s" % e)
        except RequestError as e:
            print("WARNING: Request Error: %s. Variable: %s already exists! Skipping!" % (e, var[0]) )

if __name__ == '__main__':
    balena.auth.login_with_token(os.environ["BALENA_NODE"])
    app_id = selectAppFromList()
    createDefaultBalenaENVVars(app_id)
