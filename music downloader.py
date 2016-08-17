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
        url = audio['url']
        result.append(url)
    return result

def save_audios(urls, directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
    names_pattern = "%s.mp3" % name.encode('ascii', 'ignore')
    for url in urls:
        filename = os.path.join(directory, names_pattern)
        print "Downloading %s" % filename
        open(filename, "w").write(urllib2.urlopen(url).read())

directory = None
if len(sys.argv) == 2:
    directory = sys.argv[1]
email = raw_input("Email: ")
password = getpass.getpass()
client_id = "5534383"  # Vk application ID
token, user_id = vk_auth.auth(email, password, client_id, "audio")
audios = get_audios(user_id, token)
print "\n".join("%d. %s" % (num + 1, audio["title"]) for num, audio in enumerate(audios))
choice_start = -1
choice_finish = -1
while choice_start and choice_finish not in xrange(len(audios)):
    choice_start = int(raw_input("Choose first audio to download: ")) - 1
    choice_finish = int(raw_input("Choose last audio to download: ")) - 1
if not directory:
    directory = audios[choice_start]["title"]
for choice in range(choice_start, choice_finish):
    name = audios[choice]["title"]
    audios_urls = get_audio_url(user_id, audios[choice]["aid"], token)
    save_audios(audios_urls, directory)
