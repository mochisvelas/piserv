import pymongo
import time
from datetime import datetime


client = pymongo.MongoClient()

mydb = client['testdb']
mycol = mydb['testcol']

#now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
#post = {"_id":2, "name":"eli"}
#mycol.insert_one({'datetime':'{}'.format(str(now)), 'status':'on'})

#mycol.insert_one(post)
#while True:
#    mycol.insert_one({'name':'nobody'})
#    print('reg inserted')
#    time.sleep(3)

#mycol.insert_one(post)

#res = mycol.find({"name":"Brenner"})
res = mycol.find({})
print(res)


#for r in res:
#    print(r)

