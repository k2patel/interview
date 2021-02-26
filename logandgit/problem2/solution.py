import requests, json, os


def yahoo(org, orgstring):
  url = 'https://api.github.com/search/repositories?q=' + orgstring +'%20in:name%20org:' + org
  headers = {
    'Accept': 'application/vnd.github.v3.text-match+json'
  }
  response = requests.request("GET", url, headers=headers)
  json_object = json.loads(response.text.encode('utf-8'))
  count = int(json_object.get('total_count'))
  return count

file = open(os.getcwd() + '/problem2/test_data/01-input', 'r')
lines = file.readlines()

for line in lines:
  print( line + ' ' + str(yahoo('mozilla', line) + yahoo('mozilla-services', line)))


