import requests
import hashlib

url = "https://www.westcambridgepediatrics.com/covid19"

r = requests.get(url).content
hash_object = hashlib.sha1(r)


print(hash_object)