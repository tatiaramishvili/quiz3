import requests
import json
import sqlite3
conn=sqlite3.connect('wanted_db.sqlite')
c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS wanted
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name VARCHAR (30),
             nationality VARCHAR (15),
             birth VARCHAR (25),
             race VARCHAR (15),
            )''')

res=requests.get("https://api.fbi.gov/wanted/v1/list")
result=res.json()
f=open("fbiwanted.json","w")
f.write(json.dumps(result,indent=4))
wanted_name=input("enter the name you are looking for: ")
wanted_name_new=wanted_name.upper()
info=result['items']
amount=[]
for each in info:
    if wanted_name_new in each['title']:
        count=each["title"].count(wanted_name_new)
        amount.append(count)
        if len(amount)>1:
            print('we have more than one with that name,if suggested is not the one you are looking for try to be more specific while entering the name')
        if len(amount)<=1:
            if 'subjects' in each:
                subject = (each['subjects'])
                print('he/she is wanted for: ', subject[0])
            else:
                print("why he/she is wanted is not available!")
            print("title of this case is: ", each["title"])
            if len(each['images']) >= 2:
                pre_url = (each['images'][1])
                url = pre_url['large']
                print(url)
                file = open('fbiwanted.jpg', 'wb')
                picture = requests.get(url)
                file.write(picture.content)
            elif len(each['images']) == 1:
                print("picture is not available")


#  jsonის ფაილიდან მომაქვს ძებნილების სახელები, წარმოშობა, დაბადების თარიღი(თუ არის მითითებული), და რასა
rows=[]
for every in info:
    name=every['title']
    nationality=every['nationality']
    date_of_birth=every['date_of_birth_used'][0]
    race=every['race_raw']
    row=(name,nationality,date_of_birth,race)
    rows.append(row)

c.executemany('INSERT INTO wanted (name,nationality,birth,race) VALUES (?,?,?,?)', rows)
conn.commit()

