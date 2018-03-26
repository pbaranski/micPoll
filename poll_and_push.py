#!/usr/bin/env python3
import numpy as np
import sounddevice as sd
import requests
from time import gmtime, strftime
import json

duration = 3000000
# in seconds3t

globvar = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
glob_list = []


def clear_glob_list():
    global glob_list
    glob_list = []


def add_to_glob_list(item):
    global glob_list
    glob_list.append(item)


def set_globvar_to(date):
    global globvar
    globvar = date


def audio_callback(indata, frames, time, status):
    volume_norm = int(np.linalg.norm(indata) * 10)
    # print(volume_norm)
    add_to_glob_list(volume_norm)
    # print(strftime("%Y-%m-%dT%H:%M:%S", gmtime()))
    # print("Globvar: {}".format(globvar))
    if globvar != strftime("%Y-%m-%dT%H:%M:%S", gmtime()):
        avg_v = int(sum(glob_list) / len(glob_list))
        url = "http://127.0.0.1:9200/xdelete2_sound/mic/"
        headers = {
            'Content-Type': "application/json",
        }
        payload = {'mic': avg_v, '@timestamp': globvar}
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

        # calprint('Request URL:\t{}'.format(response.url))
        # print('Request method:\t{}'.format(response.request.method))
        # print('Request headers:{}'.format(response.request.headers))
        # print('Request body:\t{}'.format(response.request.body))
        # print('Response code:\t{}'.format(response.status_code))
        # print('Response content:{}'.format(response.content))

        # print(len(glob_list))
        print(avg_v)
        clear_glob_list()
        set_globvar_to(strftime("%Y-%m-%dT%H:%M:%S", gmtime()))


stream = sd.InputStream(callback=audio_callback)
with stream:
    sd.sleep(duration * 1000)
