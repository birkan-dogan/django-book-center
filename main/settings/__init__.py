# __init__.py which is required file to create a python module

from .base import *

env_name = config("ENV_NAME")

if (env_name == "prod"):
 from .prod import *

elif (env_name == "dev"):
 from .dev import *