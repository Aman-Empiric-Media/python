from time import sleep
import requests

a = open('contract.txt')
ap = 0
api = a.readlines()
aa = len(api)
api_key = api[ap].replace('\n','')

q = open('companies.txt')
co = q.readlines()

lo = open('locations.txt')
loc = lo.readlines()

u = f"https://api.apollo.io/v1/auth/health?api_key={api_key}"

session = requests.session()
r = session.get(u)
print(r.text)

import json

# INDUSTRY SELECTION
#import json
#final = session.get(url=f'https://app.apollo.io/api/v1/tags/search?kind=linkedin_industry&display_mode=fuzzy_select_mode&per_page=200&api_key={api_key}').json()
#
#industry_id = {}
#for i in final['tags']:
#    industry_id[i['cleaned_name']] = i['id']
#
#indusind = input('Enter the keyword of industry from the textfile: ')
#indusid = []
#if indusind:
#    indusid = [industry_id[indusind]]

indu = open('industries.txt')
ind = indu.readlines()
final = session.get(url=f'https://app.apollo.io/api/v1/tags/search?kind=linkedin_industry&display_mode=fuzzy_select_mode&per_page=200&api_key={api_key}').json()

industry_id = {}
for i in final['tags']:
    industry_id[i['cleaned_name']] = i['id']

indusid = []
for indusind in ind:
    indusid.append(industry_id[indusind.replace('\n','')])

sheet = input("Enter the title of the excel sheet: ")

# TITLE SELECTION
title = input('Enter the key word to search for job title from the following: ')
final = session.get(url=f'https://app.apollo.io/api/v1/tags/search?q_tag_fuzzy_name={title}&kind=person_title&display_mode=fuzzy_select_mode&api_key={api_key}').json()
j = 0
for i in final['tags']:
    j += 1
    print(f'{j}) {i["cleaned_name"]}')
    #if j == :
    #    break

tind = input('Enter the index of key word to search for job title from the following: ')
tname = None
if tind:
    tind = tind.split(',')
    tname = []
    for i in tind:
        i = int(i)
        tname.append(final['tags'][i-1]['cleaned_name'])


# COUNTRY SELECTION
#country = input('Enter the key word to search for country from the following: ')
#final = session.get(url=f'https://app.apollo.io/api/v1/tags/search?q_tag_fuzzy_name={country}&exclude_categories[]=US State&kind=location&display_mode=fuzzy_select_mode&api_key={api_key}').json()
#countries = []
#j = 0
#for i in final['tags']:
#    j += 1
#    print(f'{j}) {i["cleaned_name"]}')
#    if j == 5:
#        break

#cind = input('Enter the index of key word to search for country from the following: ')
#cname = []
#if cind:
#    cind = int(cind)
#    cname = [final['tags'][cind-1]['cleaned_name']]

cname = []
for cn in loc:
    cname.append(cn.replace('\n',''))


# COMPANY SELECTION
#company = input('Enter the key word to search for company from the following: ')
#r = session.get(url=f'https://app.apollo.io/api/v1/organizations/search?q_organization_fuzzy_name={company}&display_mode=fuzzy_select_mode&api_key={api_key}')
#j = 0
#for i in r.json()['organizations']:
#    j += 1
#    print(f'{j}) {i["name"]}')
#    if j == 5:
#        break
#
#comind = input('Enter the index of key word to search for company from the following: ')
#comid = None
#if comind:
#    comind = int(comind)
#    comid = [r.json()['organizations'][comind-1]['id']]

comid = None
if co:
    comid = []
    
for company in co:
    company = company.replace('\n','')
    print(company)
    sleep(1.21)
    r = session.get(url=f'https://app.apollo.io/api/v1/organizations/search?q_organization_fuzzy_name={company}&display_mode=fuzzy_select_mode&api_key={api_key}')
    while r.status_code != 200 and ap < aa-1:
        print(f"Reason for {api_key} failure is {r.text}")
        api_key = api[ap+1].replace('\n','')
        ap += 1
        print(f"Api indexed to {ap+1} !")
        r = session.get(url=f'https://app.apollo.io/api/v1/organizations/search?q_organization_fuzzy_name={company}&display_mode=fuzzy_select_mode&api_key={api_key}')
    try:
        comid.append(r.json()['organizations'][0]['id'])
    except Exception as ew:
        print(f"{company} skipped please check the name",ew)


# EMPLOYEES COUNT
u = 'https://app.apollo.io/api/v1/mixed_people/facets'
d = {
    'api_key':api_key,
    "open_factor_names":["organization_num_employees_ranges"],
}
r = session.post(u,json=d).json()
j = 0
for i in r['faceting']['num_employees_facets']:
    j += 1
    print(f'{j}) {i["value"]}')

eind = input('Enter the index of key word to search for employees count from the following: ')
ecount = None
if eind:
    eind = eind.split(',')
    ecount = []
    for i in eind:
        i = int(i)
        ecount.append(r['faceting']['num_employees_facets'][i-1]['value'])

# MANAGEMENT SELECTION
u = 'https://app.apollo.io/api/v1/mixed_people/facets'
d = {
    'api_key':api_key,
    "open_factor_names":["person_seniorities"],
}
r = session.post(u,json=d).json()
j = 0
for i in r['faceting']['person_seniority_facets']:
    j += 1
    print(f'{j}) {i["value"]}')
mane = input('Enter the index of management level required: ')
p_senl = None
if mane:
    p_sen = mane.split(',')
    p_senl = []
    for i in p_sen:
        i = int(i)
        p_senl.append(r['faceting']['person_seniority_facets'][i-1]['value'])



# TECHNOLOGY SELECTION
tech_name = input('Enter the key word to search for technology from the following: ')
final = session.get(url=f'https://app.apollo.io/api/v1/tags/search?q_tag_fuzzy_name={tech_name}&kind=technology&display_mode=fuzzy_select_mode&api_key={api_key}').json()
#with open('job_titles.json',"r") as f:
#    final = json.load(f)
j = 0
tech = {}
for i in final['tags']:
    j += 1
    print(f'{j}) {i["cleaned_name"]}')
    if j == 5:
        break

techind = input('Enter the index of key word to search for technology from the following: ')
techh = []
if techind:
    techind = int(techind)
    techh = [final['tags'][techind-1]['cleaned_name']]

ma = input('Enter the maximum revenue: ')
mi = input('Enter the minimum revenue: ')
j = 1
d = {
    "api_key": api_key,
    "page": 1,
    "person_titles": tname,
    "organization_ids": comid,
    "person_locations": cname,
    "organization_num_employees_ranges": ecount,
    "organization_industry_tag_ids": indusid,
    "currently_using_any_of_technology_uids": techh,
    "person_seniorities": p_senl,
    "revenue_range": {
        "max": ma,
        "min": mi
    },
    "per_page": 50,
}
v = "https://api.apollo.io/v1/mixed_people/search"

w = session.post(v,json=d)
#print(w.json())
while w.status_code != 200  and ap < aa-1:
    print()
    print(f"Reason for {api_key} failure is {w.text}")
    api_key = api[ap+1].replace('\n','')
    ap += 1
    print(f"Api indexed to {ap+1} !")
    d = {
        "api_key": api_key,
        "page": 1,
        "person_titles": tname,
        "organization_ids": comid,
        "person_locations": cname,
        "organization_num_employees_ranges": ecount,
        "organization_industry_tag_ids": indusid,
        "currently_using_any_of_technology_uids": techh,
        "person_seniorities": p_senl,
        "revenue_range": {
            "max": ma,
            "min": mi
        },
        "per_page": 50,
    }

    
    v = "https://api.apollo.io/v1/mixed_people/search"

    w = session.post(v,json=d)
        
pages = int(w.json()['pagination']['total_pages'])
print(f'Total number of pages available are {pages}')
fin = []
#if pages >= 90:
#    pages = 90

from time import sleep
for i in range(1,pages+1):
    try:
        sleep(1)
        print(f'Getting page -->{i}')
        d = {
            "api_key": api_key,
            "page": i,
            "person_titles": tname,
            "organization_ids": comid,
            "person_locations": cname,
            "organization_num_employees_ranges": ecount,
            "organization_industry_tag_ids": indusid,
            "currently_using_any_of_technology_uids": techh,
            "person_seniorities": p_senl,
            "revenue_range": {
                "max": ma,
                "min": mi
            },
            "per_page": 50,
        }

        
        v = "https://api.apollo.io/v1/mixed_people/search"

        w = session.post(v,json=d)
        #print(w)
        while w.status_code != 200  and ap < aa-1:
            print()
            print(f"Reason for {api_key} failure is {w.text}")
            api_key = api[ap+1].replace('\n','')
            ap += 1
            print(f"Api indexed to {ap+1} !")
            print(f'Getting page -->{i+1}')
            d = {
                "api_key": api_key,
                "page": i,
                "person_titles": tname,
                "organization_ids": comid,
                "person_locations": cname,
                "organization_num_employees_ranges": ecount,
                "organization_industry_tag_ids": indusid,
                "currently_using_any_of_technology_uids": techh,
                "person_seniorities": p_senl,
                "revenue_range": {
                    "max": ma,
                    "min": mi
                },
                "per_page": 50,
            }

            
            v = "https://api.apollo.io/v1/mixed_people/search"

            w = session.post(v,json=d)
            
        fin.extend(w.json()['people'])
    except:
        print(w)
        break

fnames = []
lnames = []
linkedin_urls = []
titles = []
companies = []
company_urls = []
locations = []
employee_count = []
techie = []

links = {}
count ={}

entity = []
for i in range(len(fin)):
    try:
        fnames.append(fin[i]['first_name'])
    except:
        fnames.append('')
    try:
        lnames.append(fin[i]['last_name'])
    except:
        lnames.append('')
    try:
        linkedin_urls.append(fin[i]['linkedin_url'])
    except:
        linkedin_urls.append('')
    try:
        titles.append(fin[i]['title'])
    except:
        titles.append('')
    try:
        companies.append(fin[i]['organization']['name'])
    except:
        companies.append('')
    try:
        company_urls.append(fin[i]['organization']['website_url'])
    except:
        company_urls.append('')
    try:
        city = fin[i]['city']
        if not city:
            city = ''
        cntr = fin[i]['country']
        if not cntr:
            cntr = ''
        locations.append(city+', '+cntr)
    except:
        locations.append('')
    try:
        entity.append(fin[i]['id'])
    except:
        entity.append('')
    #vv = fin[i]['organization']['website_url']
    #if not vv:
    #    techie.append('')
    #    employee_count.append('')
    #    continue
    ##cc = r.json()['organization']['estimated_num_employees']
    #if vv in links:
    #    t = links[vv]
    #    techie.append(t)
    ##if cc in count:
    #    cv = count[vv]
    #    employee_count.append(cv)
    #else:
    #    ul = f"https://api.apollo.io/v1/organizations/enrich?api_key=XI2grxwTvjpOphQ37EZLxg&domain={vv}"
    #    r = session.get(ul)
    #    links[vv] = r.json()['organization']['industry']
    #    count[vv] = r.json()['organization']['estimated_num_employees']
    #    techie.append(links[vv])
    #    employee_count.append(count[vv])



aa = min([len(fnames),len(lnames),len(titles),len(linkedin_urls),len(companies),len(company_urls)])
import pandas as pd
dfre = pd.DataFrame(fnames,columns = ["First Name"])
dfre.insert(loc=1,value=lnames,column="Last Name")
dfre.insert(loc=2,value=titles,column="Designaton")
dfre.insert(loc=3,value=linkedin_urls,column="Linkedin Url")
dfre.insert(loc=4,value=companies,column="Company Name")
#dfre.insert(loc=5,value=employee_count,column="Employees")
#dfre.insert(loc=6,value=techie,column="Industry")
dfre.insert(loc=5,value=company_urls,column="Company Url")
dfre.insert(loc=6,value=entity,column='Emails')


dfre.to_csv(f'{sheet}.csv')

print('Done !!')
