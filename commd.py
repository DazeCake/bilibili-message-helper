import re

'''命令解析器，将命令解析为数组'''
def commandParser(cmd):
    # 检查命令是否以#开头
    if cmd[0] == '#' or cmd[0] == '/':
        # 去除#号
        cmd = cmd[1:]
        # 以空格分割命令，多个连续空格视为一个空格
        cmd = re.split(r'\s+', cmd)
        # 去除空格
        cmd = [i for i in cmd if i != '']
        return cmd
    else:
        return None

