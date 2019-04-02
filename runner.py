##################################
# Antone M King                  #
# Pull Down all records & fields #
##################################

import requests
import json
import pprint
import config
import pandas as pd

#Download JSON data with JSONv2 manually if you are running > 1000 records
#After saving to root convert the json data into an excel file

'''
data_parsed = json.loads(open('FULL PATH/attachment-runner-procurement/ast_contract_procurement.json', encoding="utf-8").read())
df = pd.DataFrame.from_dict(data_parsed['records'], orient='columns')
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, 'sheet1')
writer.save()
'''
#Use if < 1000 Records
#TODO: add offset for REST query to paginate queries greater than 1000

usr = config.username
pwd = config.password
table = config.table
query = config.query
url = config.URI + "/api/now/table/"+table+"?sysparm_exclude_reference_link=true&sysparm_query="+query
headers = {"content-Type": "application/json"}
r = requests.get(url, auth=(usr, pwd), headers=headers)
if r.status_code != 200:
    print('Status:', r.status_code, 'Headers:', r.headers, 'Error Response:',r.json())
    exit()
data = r.json()
df = pd.DataFrame.from_dict(data['result'], orient='columns')
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, 'sheet1')
writer.save()
        
print("")
print("COMPLETE! Transform file has finished downloading. You can now run \"python zipPull.py\"")
