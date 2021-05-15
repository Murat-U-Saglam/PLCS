import os

import requests
import pickle


def startSession():
    global s
    s = requests.Session()


def getCookies(URL):
    r = s.get(URL)
    print(r.cookies)


def setCookies(URL, cookieName, cookieValue):
    s.post(URL, params={cookieName: cookieValue})


def wipeCookies():
    global s
    s = requests.Session()


# https://www.youtube.com/watch?v=2Tw39kZIbhs
def saveCookieSession(URL):
    r = s.get(URL)
    path = os.getcwd()
    pickle_out = open(path + '/PersistentCookies/SavedCookies', "wb")
    pickle.dump(r.cookies, pickle_out)
    pickle_out.close()


# https://www.youtube.com/watch?v=2Tw39kZIbhs
def restoreCookieSession(URL):
    r = s.get(URL)
    path = os.getcwd()
    pickle_in = open(path + '/PersistentCookies/SavedCookies', "rb")
    r.cookies = pickle.load(pickle_in)
    pickle_in.close()
