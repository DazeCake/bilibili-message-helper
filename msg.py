import config
import time
import json
import requests
import login


def getUser(uid):
    rdata = {
        "uids": uid
    }
    res = requests.get(
        'https://api.vc.bilibili.com/account/v1/user/cards', params=rdata)
    return json.loads(res.text)['data'][0]


def getChatList() -> dict:
    rdata = {
        "sender_device_id": 1,
        "talker_id": config.account['DedeUserID'],
        "session_type": 1,
        "size": 20,
        "build": 0,
        "mobi_app": "web"
    }
    rcookies = {
        "SESSDATA": config.account['SESSDATA']
    }
    res = requests.get(
        'https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions', params=rdata, cookies=rcookies)
    if json.loads(res.text)['code'] == 0:
        return json.loads(res.text)
    else:
        login.login()
        return getChatList()


def getNewMsg():
    chatList = getChatList()["data"]["session_list"]
    newChat = [i for i in chatList if i["unread_count"] > 0]
    return newChat


def getDetail(talker_id):
    rdata = {
        "sender_device_id": 1,
        "talker_id": talker_id,
        "session_type": 1,
        "size": 20,
        "build": 0,
        "mobi_app": "web"
    }
    rcookies = {
        "SESSDATA": config.account['SESSDATA']
    }
    res = requests.get(
        'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs', params=rdata, cookies=rcookies)
    return json.loads(res.text)


def readMsg(talker_id, ack_seqno=0):
    rcookies = {
        "SESSDATA": config.account['SESSDATA']
    }
    rdata = {
        "talker_id": talker_id,
        "session_type": 1,
        # "ack_seqno": ack_seqno,
        "build": 0,
        "mobi_app": "web"
    }
    res = requests.get(
        f'https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack', cookies=rcookies, params=rdata)


def sendMsg(receiver_id, content):
    # curl 'http://api.vc.bilibili.com/web_im/v1/web_im/send_msg' \
    #     - -data-urlencode 'msg[sender_uid]=293793435' \
    #     - -data-urlencode 'msg[receiver_id]=1' \
    #     - -data-urlencode 'msg[receiver_type] =1' \
    #     - -data-urlencode 'msg[msg_type]=1' \
    #     - -data-urlencode 'msg[dev_id] =372778FD-E359-461D-86A3-EA2BCC6FF52A' \
    #     - -data-urlencode 'msg[timestamp] =1626181379' \
    #     - -data-urlencode 'msg[content]={"content":"up主你好，\n催更[doge]"}' \
    #     - -data-urlencode 'csrf=xxx' \
    #     - b 'SESSDATA=xxx'
    rcookies = config.account
    rdata = {
        "msg[sender_uid]": config.account['DedeUserID'],
        "msg[receiver_id]": receiver_id,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        # 可以用login.py里的getDeviceId()获取
        "msg[dev_id]": "14885AF4-31BC-4CE2-97A7-23CA06FFA1B5",
        "msg[timestamp]": int(time.time()),
        "msg[content]": '{"content": "'+content+'"}',
        "csrf_token": config.account['bili_jct'],
        "csrf": config.account['bili_jct']
    }
    rheaders = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(
        'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg', data=rdata, cookies=rcookies, headers=rheaders)
    return res.json()['code'] == 0
