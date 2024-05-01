import pymysql as sql

class profiles_db:
    def __init__(self) -> None:
        self.mysql = sql.connect(database="graduate_db", user="GraduateEntrepreneurAdminLogin",
                                    password="ThisIsThePasscodeForTheSourcingSQLDatabaseForSourcingPurposesAndMore123!",
                                    host="graduateentrepreneurserver.mysql.database.azure.com", port=3306,
                                    ssl={'ca': '/Users/jandomhof/Documents/DigiCertGlobalRootCA.crt.pem'})

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

    def close(self) -> None:
        self.cursor.close()
        self.mysql.close()

    def insert(self, founders) -> None:
        founder_tuples = [(founder["Name"], founder["Linkedin"], founder["Title"], founder["University"], founder["Year"], founder["TitleIndicatesFounder"], founder["InEdda"], founder["MatchingEddaWord"], founder["Assignee"], founder["Checked"], founder["AddedToEdda"]) for founder in founders]
        columns = "Name, Linkedin, Title, University, Year, TitleIndicatesFounder, InEdda, MatchingEddaWord, Assignee, Checked, AddedToEdda"
        query = f"INSERT INTO li_profiles ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.executemany(query, founder_tuples)
        self.mysql.commit()
        print(f"Committed {len(founders)} profiles")

    def fetch_assignees(self, names) -> dict:
        assignees = {}
        for name in names:
            self.cursor.execute(f'SELECT COUNT(*) FROM li_profiles WHERE Assignee="{name}" AND Checked=0 AND TitleIndicatesFounder=1')
            records = self.cursor.fetchall()
            assignees[name] = int(records[0][0])

        return assignees