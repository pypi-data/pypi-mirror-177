import __main__
import os
import re

default_config = '''
{
    "ip": "default",
    "port": 5000,
    "queue_size": 10,
	"SSL": false,
	"cert_path" : "",
	"key_path" : ""
}
'''

main_path = "/".join(re.split('/|\\\\',os.path.dirname(__file__))[:-1])

if not os.path.exists(main_path):
    os.makedirs(main_path + "/content")
    
if not os.path.exists(main_path + "/config"):
    os.makedirs(main_path + "/config")
    
if not os.path.exists(main_path + "/config/config.json"):#
    with open(main_path + "/config/config.json", 'w') as config:
        config.writelines(str(default_config))

from .webserver import *