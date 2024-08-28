import pymysql as sql
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

class profiles_db:
    def __init__(self) -> None:
        self.open_connection()

    def open_connection(self):
        self.mysql = sql.connect(database="graduate_db", user=os.environ["DB_USERNAME"],
                                    password=os.environ["DB_PASSWORD"],
                                    host="graduateentrepreneurserver.mysql.database.azure.com", port=3306,
                                    ssl={'ca': os.environ["SSL_LOCATION"]})

        # create cursor
        self.cursor = self.mysql.cursor()

    def fetch_names(self) -> list:
        # fetch all queries and save in pandas df
        self.cursor.execute("SELECT Name FROM li_profiles")
        records = self.cursor.fetchall()
        return [record[0] for record in records]
    
    def fetch_linkedin_urls(self) -> list:
        # fetch all queries and save in pandas df
        self.cursor.execute("SELECT Linkedin FROM li_profiles")
        records = self.cursor.fetchall()
        return [record[0] for record in records]
    
    def fetch_name_li_title(self) -> list:
        # fetch all queries and save in pandas df
        query = "SELECT Name, Linkedin, Title FROM li_profiles"
        return pd.read_sql(query, self.mysql)

    def close(self) -> None:
        self.cursor.close()
        self.mysql.close()

    def insert(self, founders) -> int:
        founder_tuples = [(founder["Name"], founder["Linkedin"], founder["Title"], founder["University"], founder["Year"], founder["TitleIndicatesFounder"], founder["InEdda"], founder["MatchingEddaWord"], founder["Assignee"], founder["Checked"], founder["AddedToEdda"]) for founder in founders]
        columns = "Name, Linkedin, Title, University, Year, TitleIndicatesFounder, InEdda, MatchingEddaWord, Assignee, Checked, AddedToEdda"
        query = f"INSERT INTO li_profiles ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE Linkedin=VALUES(Linkedin);"
        self.cursor.executemany(query, founder_tuples)
        self.mysql.commit()
        return len(founders)

    def update_record(self, name, title, linkedin):
        query = f'UPDATE li_profiles SET Name="{name}", Title="{title}", Checked=0 WHERE LinkedIn LIKE "{linkedin}%"'
        self.cursor.execute(query)
        self.mysql.commit()

    def fetch_assignees(self, names) -> dict:
        assignees = {}
        for name in names:
            self.cursor.execute(f'SELECT COUNT(*) FROM li_profiles WHERE Assignee="{name}" AND Checked=0 AND TitleIndicatesFounder=1')
            records = self.cursor.fetchall()
            assignees[name] = int(records[0][0])

        return assignees
    
    def fetch_name(self, li):
        self.cursor.execute(f'SELECT Name FROM li_profiles WHERE Linkedin LIKE "{li}%"')
        record = self.cursor.fetchone()
        return str(record[0])
    
    def fetch_title(self, li):
        self.cursor.execute(f'SELECT Title FROM li_profiles WHERE Linkedin LIKE "{li}%"')
        record = self.cursor.fetchone()
        return str(record[0])