import vk_auth
import json
import urllib2
from urllib import urlencode
import os
import getpass
import sys

def call_api(method, params, token):
    params.append(("access_token", token))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
    return json.loads(urllib2.urlopen(url).read())["response"]

def get_audios(user_id, token):
    return call_api("audio.get", [("uid", user_id)], token)

def get_audio_url(user_id, audio_id, token):
    audios_list = call_api("audio.get", [("uid", user_id), ("aid", audio_id)], token)
    result = []
    for audio in audios_list:
        url = audio["url"]
        result.append(url)
    return result

def save_audios(url, directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    names_pattern = "%s.mp3" % name.encode('ascii', 'ignore')
    filename = os.path.join(directory, names_pattern)
    print "Downloading %s" % filename
    open(filename, "wb").write(urllib2.urlopen(url).read())

directory = None
if len(sys.argv) == 2:
    directory = sys.argv[1]
#email = raw_input("Email: ")
#password = getpass.getpass()
email = "kat.kat.3@ya.ru"
password = "443233082zx"
client_id = "5534383"  # Vk application ID
token, user_id = vk_auth.auth(email, password, client_id, "audio")
audios = get_audios(user_id, token)
print "\n".join("%d. %s" % (num + 1, audio["title"]) for num, audio in enumerate(audios))
choice = -1
while choice not in xrange(len(audios)):
    choice = int(raw_input("Choose audio number: ")) - 1
if not directory:
    directory = audios[choice]["title"]
name = audios[choice]["title"]
#aid = str(audios[choice]["aid"]) + ','
audios_url = get_audio_url(user_id, audios[choice]["aid"], token)
save_audios(audios_url, directory)
print "Completed"