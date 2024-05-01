import requests
import json
import os

class Edda:
    def __init__(self):
        self.url = "https://eu-dealflow.edda.co"
        payload = {
                "email": os.environ["EDDA_USERNAME"],
                "password": os.environ["EDDA_PASSWORD"]
        }
        endpoint = "/api/v2/auth/login"
        response = self.post(self.url + endpoint, payload)
        self.token = json.loads(response.text)['data']['access_token']

    def post(self, url, payload):
        return requests.post(url, json=payload, headers={"Accept": "application/json"})
    
    def get(self, url, auth):
        return requests.get(url, headers={"Accept": "application/json", "Authorization": f"Bearer {auth}"})
    
    def get_company_fields(self, workspace, company) -> list:
        endpoint = f"/api/v2/{workspace}/companies/{company}/info"
        return json.loads(self.get(self.url + endpoint, self.token).text)["data"]
    
    def get_company_vertical(self, workspace, company) -> list:
        endpoint = f"/api/v2/{workspace}/companies/{company}/info"
        return json.loads(self.get(self.url + endpoint, self.token).text)["data"][30]["value"]["name"]

    
    def get_companies(self) -> list:
        workspace = "864" # Graduate workspace id
        pipeline = "1683" # Pre-Seed pipeline id
        endpoint = f"/api/v2/{workspace}/pipelines/{pipeline}/companies"
        # endpoint = f"/api/v2/{workspace}/companies"

        companies = json.loads(self.get(self.url + endpoint, self.token).text)["data"]

        return [{"name": company["name"],
                 "description": company["description"],
                #  "vertical": self.get_company_fields(workspace, company["id"])["value"]["name"] if self.get_company_fields(workspace, company["id"])["value"] else None,
                 "column":company["stage"]["name"],
                 "assignees": [owner["firstname"] for owner in company["owners"]]                 
                 } for company in companies]


    def get_company_by_name(self, name):
        workspace = "864" # Graduate workspace id
        endpoint = f"/api/v2/{workspace}/companies/search"
        payload = {
            "search": name,
            "fuzzy": 1
        }
        return json.loads(requests.get(self.url + endpoint, params=payload, headers={"Accept": "application/json", "Authorization": f"Bearer {self.token}"}).text)["data"]
    
    def get_company_by_id(self, id):
        workspace = "864"
        endpoint = f"/api/v2/{workspace}/companies/{id}"
        return json.loads(requests.get(self.url + endpoint, headers={"Accept": "application/json", "Authorization": f"Bearer {self.token}"}).text)["data"]
    
    def check_in_edda_by_name(self, name):
        res = self.get_company_by_name(name)
        if len(res) > 0:
            for r in res:
                if r["pipeline"]["id"] == 1683 or r["pipeline"]["id"] == 2053:
                    return r
                
            return None

    def get_edda_link(self, name):
        json = self.check_in_edda_by_name(name)
        return f"https://eu-dealflow.edda.co/864/{json["pipeline"]["id"]}/company/{json["id"]}"