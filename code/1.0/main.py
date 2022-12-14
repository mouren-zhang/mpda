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
        nbtfile = nbtfile.replace('[', '').replace(']', '').split(',')

        # 列表转dict
        nbtfile = str(nbtfile)[1:-1].replace('):', ')":"')
        nbtfile = json.loads('{' + nbtfile + '}')

        # 玩家游戏模式统计
        if nbtfile.get("TAG_Int('playerGameType')") == '0':
            list_mod0.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '1':
            list_mod1.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '2':
            list_mod2.append(len_uuid(i))
        elif nbtfile.get("TAG_Int('playerGameType')") == '3':
            list_mod3.append(len_uuid(i))

        if prmod:
            # 筛查模式

            playerGameType = get_playerGameType(nbtfile, "TAG_Int('playerGameType')")

            xpLevel = nbtfile.get(nbtfile, "TAG_Int('XpLevel')")

            world = get_world(nbtfile, "TAG_String('Dimension')")

            Health = nbtfile.get(nbtfile, "TAG_Float('Health')")

            XpTotal = nbtfile.get(nbtfile, "TAG_Int('XpTotal')")

            seenCredits = get_seenCredits(nbtfile, "TAG_Byte('seenCredits')")

            FallFlying = get_FallFlying(nbtfile, "TAG_Byte('FallFlying')")

            FallDistance = nbtfile.get(nbtfile, "TAG_Float('FallDistance')")

            HurtByTimestamp = nbtfile.get(nbtfile, "TAG_Int('HurtByTimestamp')")

            SleepTimer = nbtfile.get(nbtfile, "TAG_Short('SleepTimer')")

            Invulnerable = nbtfile.get(nbtfile, "TAG_Byte('Invulnerable')")




            PortalCooldown = nbtfile.get("TAG_Int('PortalCooldown')")

            AbsorptionAmount = nbtfile.get("TAG_Float('AbsorptionAmount')")

            DeathTime = nbtfile.get("TAG_Short('DeathTime')")

            foodSaturationLevel = nbtfile.get("TAG_Float('foodSaturationLevel')")

            foodExhaustionLevel = nbtfile.get("TAG_Float('foodExhaustionLevel')")

            OnGround = nbtfile.get("TAG_Byte('OnGround')")

            Score = nbtfile.get("TAG_Int('Score')")

            Fire = nbtfile.get("TAG_Short('Fire')")

            XpP = nbtfile.get("TAG_Float('XpP')")

            DataVersion = nbtfile.get("TAG_Int('DataVersion')")

            foodLevel = nbtfile.get("TAG_Int('foodLevel')")

            foodTickTimer = nbtfile.get("TAG_Int('foodTickTimer')")

            HurtTime = nbtfile.get("TAG_Short('HurtTime')")

            XpSeed = nbtfile.get("TAG_Int('XpSeed')")

            SelectedItemSlot = nbtfile.get("TAG_Int('SelectedItemSlot')")

            Air = nbtfile.get("TAG_Short('Air')")

            d = {
                '游戏模式': playerGameType,
                '经验等级': xpLevel,
                '经验总数': XpTotal,
                '所处世界': world,
                '健康状态': Health,
                '去过下界': seenCredits,
                '是否飞行': FallFlying,
                '时间伤害': HurtByTimestamp,
                '入睡经过': SleepTimer,
                '坠落距离': FallDistance,
                '抵消伤害': Invulnerable,
                '传送门冷却': PortalCooldown,
                '伤害吸收': AbsorptionAmount,
                '死亡时间': DeathTime,
                '当前饱食度': foodLevel,
                '饱回血间隔': foodTickTimer,
                '饱和度等级': foodSaturationLevel,
                '饥饿度等级': foodExhaustionLevel,
                '是否在地上': OnGround,
                '死亡分数': Score,
                '升级百分比': XpP,
                '游戏版本': DataVersion,
                '附魔台种子': XpSeed,
                '右手槽位': SelectedItemSlot,
                '头在方块？': Air,
                '火焰伤害？': Fire,
                '持续伤害？': HurtTime,
            }

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



def get_FallFlying(nbt, key):
    a = nbt.get(key)

    if a == '1':

        return '是'
    elif a == '0':
        return '否'
    else:
        return '未知/出错'


def get_seenCredits(nbt, key):
    yn = nbt.get(key)

    if yn == '1':
        return '去过'

    elif yn == '0':
        return '还没'

    else:
        return '未知'




def get_world(nbt, key):
    world = nbt.get(key)

    if world == 'minecraft:overworld':
        world = '主世界'
    elif world == 'minecraft:the_nether':
        world = '下界(地狱)'
    elif world == 'minecraft:the_end':
        world = '末地'

    return world


def get_playerGameType(nbt, key):
    # 取游戏模式
    playerGameType_mod = nbt.get(key)

    if playerGameType_mod == '0':
        playerGameType = '生存'
    elif playerGameType_mod == '1':
        playerGameType = '创造'
    elif playerGameType_mod == '2':
        playerGameType = '冒险'
    elif playerGameType_mod == '3':
        playerGameType = '旁观'
    else:
        playerGameType = '获取失败'

    return playerGameType


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
        '0': '统计模式',
        '1': '筛查模式'
    }
    for k, v in pr_dt.items():
        print(k, v)
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
