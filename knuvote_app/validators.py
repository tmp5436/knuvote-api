import logging
import re
from datetime import date

import requests

from knuvote_app.enums import Provider
logger = logging.getLogger(__name__)

class Validators():

    def userValidate(user):
        if user.username is None or user.email is None or user.password is None:
            return False
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", user.email):
            return False
        if len(user.username) < 3 or len(user.password) < 8:
            return False
        return True

    def categoryValidate(category):
        if category.name is None or category.expiration_time is None:
            return False
        if len(category.name) < 3 or category.expiration_time <= date.today().strftime("%Y-%m-%d"):
            return False
        return True

    def accessTokenValidate(requestData):
        if Provider[requestData['provider']] is Provider.FACEBOOK:
            URL = "https://graph.facebook.com/me"
            PARAMS = {'access_token': requestData['authToken']}
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            return data['id'] == requestData['id']
        elif Provider[requestData['provider']] is Provider.GOOGLE:
            URL = "https://oauth2.googleapis.com/tokeninfo"
            PARAMS = {'id_token': requestData['idToken']}
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            return data['sub'] == requestData['id']
        else:
            return False