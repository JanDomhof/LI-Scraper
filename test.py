from db import profiles_db

db = profiles_db()
print(db.fetch_names())