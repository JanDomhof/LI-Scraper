from db import profiles_db
import os

report_count = max([int(f.split(" ")[-1].split(".")[0]) for f in os.listdir("./reports")])

print(report_count)