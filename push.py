from faunadb.client import FaunaClient
from faunadb import query as q
from dotenv import load_dotenv
import json
import os

load_dotenv()

secret = os.getenv("secret")
client = FaunaClient(secret=secret)
coll = 'daily'

# open json file created by format routine
with open('data/daily.json', 'r')as file:
	data = json.load(file)
	json_data = json.loads(data)

# Adds new record
client.query(q.create(q.collection(coll),{'data': json_data}))

# Prunes duplicate records
documents = client.query(q.paginate(q.documents(q.collection(coll))))
unique_first_keys = {}
documents_to_delete = []
for document_ref in documents["data"]:
	document = client.query(q.get(document_ref))
	first_key_name = list(document["data"].keys())[0]
	if first_key_name in unique_first_keys:
		documents_to_delete.append(q.ref(q.collection(coll), document_ref.id()))
	else:
		unique_first_keys[first_key_name] = document_ref
count = len(documents_to_delete)	
for doc_ref in documents_to_delete:
	client.query(q.delete(doc_ref))


print(f'{count} records have been pruned')
print('Data Uploaded')