from db import profiles_db
import os

db = profiles_db()
db_records = db.fetch_name_li_title()
print(db_records['Linkedin'])

print(db_records['Linkedin'].str.contains("https://www.linkedin.com/in/jop-kokkedee-42697a72").any())
"https://www.linkedin.com/in/jobsesink"