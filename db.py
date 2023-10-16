import pymysql as sql

class profiles_db:
    def __init__(self) -> None:
        self.mysql = sql.connect(database="graduate_db", user="GraduateEntrepreneurAdminLogin",
                                    password="ThisIsThePasscodeForTheSourcingSQLDatabaseForSourcingPurposesAndMore123!",
                                    host="graduateentrepreneurserver.mysql.database.azure.com", port=3306,
                                    ssl={'ca': '/Users/janjr/DigiCertGlobalRootCA.crt.pem'})

        # create cursor
        self.cursor = self.mysql.cursor()

    def fetch_names(self) -> list:
        # fetch all queries and save in pandas df
        self.cursor.execute("SELECT Name FROM profiles_db")
        records = self.cursor.fetchall()
        return [record[0] for record in records]
    
    def close(self) -> None:
        self.cursor.close()
        self.mysql.close()

    def insert(self, founders) -> None:
        founder_tuples = [(founder.name, founder.linkedin, founder.title, founder.university, founder.year, founder.title_indicates_founder, founder.in_edda, founder.matching_edda_word, founder.assignee, founder.checked, founder.added_to_edda) for founder in founders]
        columns = "Name, Linkedin, Title, University, Year, TitleIndicatesFounder, InEdda, MatchingEddaWord, Assignee, Checked, AddedToEdda"
        query = f"INSERT INTO profiles_db ({columns}) VALUES (%s, %s, %s)"
        self.cursor.executemany(query, founder_tuples)
        self.mysql.commit()

    def fetch_assignees(self) -> dict:
        self.cursor.execute("SELECT Assignee, COUNT(*) as count FROM profiles_db GROUP BY Assignee ORDER BY count ASC")
        records = self.cursor.fetchall()
        return {rec[0]: rec[1] for rec in records}
