import time
import msg
import json
import config

# 每30s检查一次未读消息
timeInterval = 30

config.loadConfig()
print("私信监听已启动，当前监听间隔为" + str(timeInterval) + "s")
while True:
    unReadMsgList = msg.getNewMsg()
    for unReadMsg in unReadMsgList:
        talker_id = unReadMsg['talker_id']
        talker_name = msg.getUser(talker_id)['name']
        last_msg = json.loads(unReadMsg['last_msg']['content'])['content']
        print(f"[{talker_name}] --> {last_msg}")
        # todo: 处理消息
        msg.sendMsg(talker_id, "收到")
        msg.readMsg(talker_id)
    time.sleep(timeInterval)
