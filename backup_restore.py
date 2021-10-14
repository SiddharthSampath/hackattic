import requests
import base64
import psycopg2

resp = requests.get("https://hackattic.com/challenges/backup_restore/problem?access_token=bb2253e1952b8d10")
resp_json = resp.json()

# the string is base64 encoded, so first decode it and write to a file
dump_str = resp_json['dump']
decode_str = base64.b64decode(dump_str)
with open("d4.dump", 'wb') as f:
    f.write(decode_str)

# the db dump is also z9 compressed so it can be uncompressed using gunzip
#  gunzip -c d4.dump | psql dump
# the above command restores the dump into a db called dump

conn = psycopg2.connect("dbname=dump user=siddharthsampath")
cur = conn.cursor()

cur.execute("select ssn from criminal_records where status='alive';")
recs = cur.fetchall()
rec_list = [rec[0] for rec in recs]

json = {'alive_ssns': rec_list}
resp = requests.post('https://hackattic.com/challenges/backup_restore/solve?access_token=bb2253e1952b8d10', json=json)

resp_res = resp.text