import yaml

account = {
    'SESSDATA': '',
    'DedeUserID': '',
    'DedeUserID__ckMd5': '',
    'bili_jct': '',
    'sid': '',
}


def loadConfig():
    global account
    file = open('config.yml', 'r', encoding="utf-8")
    file_data = file.read()
    account = yaml.load(file_data, Loader=yaml.FullLoader)
    file.close()


def saveConfig():
    file = open('config.yml', 'w', encoding="utf-8")
    file.write(yaml.dump(account))
    file.close()

