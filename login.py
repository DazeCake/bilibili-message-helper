import random
import config
import requests
import qrcode
import io

session = requests.session()


def generateDeviceID():
    b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    s = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    s = list(s)
    for i in range(len(s)):
        if s[i] == '-' or s[i] == '4':
            continue
        randomInt = random.randint(0, 15)
        if s[i] == 'x':
            s[i] = b[randomInt]
        else:
            s[i] = b[3 & randomInt | 8]
    return ''.join(s)

def applyQRCode():
    r = session.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header')
    rjson = r.json()
    qr = qrcode.QRCode(border=0)
    qr.add_data(rjson['data']['url'])
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
    print(rjson['data']['url'])
    return rjson['data']['qrcode_key']


def scanCodeToLogIn(qrcode_key):
    rdata = {
        'qrcode_key': qrcode_key,
        'source': 'main-fe-header'
    }
    session.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/poll', params=rdata)
    return None


def login():
    qrcode_key = applyQRCode()
    input("扫码后继续")
    scanCodeToLogIn(qrcode_key)
    for cookieKey in session.cookies.keys():
        config.account[cookieKey] = session.cookies.get(cookieKey)
    config.saveConfig()


# login()
# print(generateDeviceID())
