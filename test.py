from db import profiles_db
import os
import re
import string
import requests
import numpy as np
from tabulate import tabulate
import json

from dotenv import load_dotenv
load_dotenv()


a = [['==', '==', '==', '=='],['test', 4, 5, 6]]
print(a[-1][1:])