e = open('ent.txt')
en = e.readlines()

a = open('email_contract.txt')
api_key = a.readlines()[0]

entity = []

for i in en:
    f = i.replace('\n','')
    entity.append(f)

import requests

session = requests.session()

emails = []

for i in range(len(entity)):
    url = 'https://app.apollo.io/api/v1/mixed_people/add_to_my_prospects'
    d = {"entity_ids":[entity[i]],
        "analytics_context":"Person Sidebar",
        "cta_name":"Access Email",
        "api_key":api_key
    }

    r = session.post(url,json=d)
    try:
        email = r.json()['contacts'][0  ]['email']
        if email:
            emails.append(email)
        else:
            emails.append("None")
        print(f"{i+1}-->Emails done!")
    except Exception as ew:
        print(f"{entity[i]} skipped",ew)
        emails.append('None')
import pandas as pd
dfre = pd.DataFrame(emails,columns = ["Emails"])
dfre.insert(loc=1,value=entity,column="Entity")
dfre.to_csv('Emails.csv')