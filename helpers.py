import json
import requests

from config import DefaultConfig


def sendPush(message):
    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic " + DefaultConfig.ONESIGNAL_KEY}
    payload = {"app_id": DefaultConfig.ONESIGNAL_APP_ID,
               "included_segments": ["All"],
               "contents": {"en": message}}
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))


def logEvent(endpoint, payload, id=None):
    if id:
        req = requests.patch(DefaultConfig.FIREBASE_URL + endpoint + '.json', data=json.dumps(payload))
    else:
        req = requests.post(DefaultConfig.FIREBASE_URL + endpoint + '.json', data=json.dumps(payload))
    return req.json()