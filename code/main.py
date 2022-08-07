import re
import glob
from nbt import nbt
import requests
import json

# # 全局变量
# 文件路径列表
lis = []
# 显示模式
prmod = 0  # 0仅显示数量 1显示数量+uuid
data = {}

def main():
    """
    主函数
    :return:None
    """
    global data


    add_w()
    list_mod0 = []  # 生存模式
    list_mod1 = []  # 创造模式
    list_mod2 = []  # 冒险模式
    list_mod3 = []  # 旁观模式

    # 从列表获取文件路径
    for i in lis:
        nbtfile = nbt.NBTFile(i, 'rb')


        # 虽然恶臭，又不是不能用【狗头】

        # 转列表
        nbtfile = str(nbtfile)[1:-1].replace(' ', '').replace('{', '').replace('}', '')
        nbtfile = nbtfile.replace('[', '').replace(']','').split(',')

        # 列表转dict
        nbtfile = str(nbtfile)[1:-1].replace('):', ')":"')
        nbtfile = json.loads('{'+nbtfile+'}')


        # 玩家游戏模式统计
        if nbtfile.get("TAG_Int('playerGameType')") == '0':
            list_mod0.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '1':
            list_mod1.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '2':
            list_mod2.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '3':
            list_mod3.append(len_uuid(i))

        if prmod :
            # 筛查模式

            # 取游戏模式
            if nbtfile.get("TAG_Int('playerGameType')") == '0':
                playerGameType='生存'
            elif nbtfile.get("TAG_Int('playerGameType')") == '1':
                playerGameType='创造'
            elif nbtfile.get("TAG_Int('playerGameType')") == '2':
                playerGameType='冒险'
            elif nbtfile.get("TAG_Int('playerGameType')") == '3':
                playerGameType='旁观'


            world = nbtfile.get("TAG_String('Dimension')")
            if world == 'minecraft:overworld':
                world = '主世界'
            elif world == 'minecraft:the_nether':
                world = '下界(地狱)'
            elif world == 'minecraft:the_end':
                world = '末地'

            d = {
                '游戏模式':playerGameType,
                '经验等级':nbtfile.get("TAG_Int('XpLevel')"),
                '所处世界':world
            }
            # print(len_uuid(i))

            data[str(len_uuid(i))] = d
        else:
            # 统计模式
            data = {
                '生存': str(len(list_mod0)),
                '创造': str(len(list_mod1)),
                '冒险': str(len(list_mod2)),
                '旁观': str(len(list_mod3)),
            }

    return data



def updata():
    """
    更新检查
    :return:
    """

    V = 1.20
    url = 'https://mouren-zhang.github.io/index.json'
    # url = 'http://127.0.0.1/mpda/index.json'

    headers = {
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return 'no'

    # 版本比对
    Version = r.json().get('mpda', {}).get('Version')

    if Version == None or Version == '':
        return 'no'

    if Version > V:
        # 有变动
        print('当前版本为', V, '最新版本', Version)

        title = r.json().get('mpda', {}).get('title')
        print(title)

        text = r.json().get('mpda', {}).get('text')
        for i in text:
            print(i)

        print('#' * 10)
    return 'ok'


def len_uuid(filename):
    """
    从字符串中提取uuid
    :param filename: str
    :return: uuid
    """
    return re.compile(r'playerdata\\(.*).dat', re.MULTILINE).findall(filename)[0]


def add_w():
    """
    获取全部数据
    :return: dict
    """

    global lis
    # 文件路径
    ml = r'C:\Users\zhang\Desktop\玩家存档分析\playerdata'
    # ml = r'playerdata'

    # 获取路径下每个文件的文件路径加入列表
    for filename in glob.glob(ml + '\*.dat'):

        # 判断文件名长度是否合法 uuid长度不合法的就跳过
        if len(len_uuid(filename)) != 36:
            continue
        # 合法文件加入列表
        lis.append(filename)
    print('加载数据', len(lis), '个')



if __name__ == '__main__':
    try:
        if updata() == 'no':
            print('检查更新失败，请自行确认更新\nhttps://github.com/mouren-zhang/mpda')
    except:
        print('检查更新失败，请自行确认更新\nhttps://github.com/mouren-zhang/mpda')
    
    print('使用须知\n请不要用本程序去检索热文件，若因为使用不当造成的由使用者承担')

    pr_dt = {
        '0':'统计模式',
        '1':'筛查模式'
    }
    for k,v in pr_dt.items():
        print(k,v)
    a = input('$:')
    # a = '0'
    if a == '0':
        prmod = 0
    elif a == '1':
        prmod = 1
    else:
        print('输入有误，默认统计模式')
        prmod = 0

    print(main())
