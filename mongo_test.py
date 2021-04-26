import pymongo
import time

client = pymongo.MongoClient()

mydb = client['testdb']
mycol = mydb['testcol']
#post = {"_id":2, "name":"eli"}

while True:
    mycol.insert_one({'name':'nobody'})
    print('reg inserted')
    time.sleep(3)

#mycol.insert_one(post)
#mycol.insert_one(post)

#res = mycol.find({"name":"Brenner"})
#res = mycol.find({})


#for r in res:
#    print(r)

