import requests, json, os


def yahoo(org, orgstring):
  url = 'https://api.github.com/orgs/'+ org + '/repos'
  payload = {}
  headers = {
    'Accept': 'application/vnd.github.v3+json'
  }
  response = requests.request("GET", url, headers=headers, data = payload)
  json_object = json.loads(response.text.encode('utf-8'))
  k=0
  count = 0
  while k < len(json_object):
    if json_object[k]['name'] == orgstring:
       count += 1
   
  k += 1
  return count

file = open(os.getcwd() + '/test_data/01-input', 'r')
lines = file.readlines()
count = 0

for line in lines:
  print('line ' + yahoo('mozilla', line) + yahoo('mozilla-services', line))


