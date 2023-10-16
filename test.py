from db import profiles_db
import pandas as pd
from edda import Edda
import requests
import json

e = Edda()
e.auth()
companies = e.get_company_fields(864, 550557)
print(companies)
