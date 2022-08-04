import re
import glob
import requests
from nbt import nbt


lis = []
prmod = 0  

def updata():
    """
    更新检查
    :return:
    """

    V = 1.13
    url = 'https://mouren-zhang.github.io/index.json'
    
    headers = {
        'Connection': 'close',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'
    }
    r = requests.get(url, headers=headers)
    Version = r.json().get('mpda', {}).get('Version')

    if Version != V:
        print('当前版本为', V, '最新版本', Version)

        title = r.json().get('mpda', {}).get('title')
        print(title)

        text = r.json().get('mpda', {}).get('text')
        for i in text:
            print(i)
        print('#'*10)
    
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
    

    ml = r'playerdata'
    ml1 = r'D:\Desktop\mc\.minecraft\versions\1.19-Fabric 0.14.8\saves\001\playerdata'
    ml2 = r'D:\Desktop\py\mc\玩家存档分析\playerdata'

    
    for filename in glob.glob(ml2 + '\*.dat'):

        
        if len(len_uuid(filename)) != 36:
            continue
        
        lis.append(filename)
    print('加载数据', len(lis), '个')


def dat(name, nbtfile):
    '''
    提取值
    :param dt:数据列表
    :return: 值
    '''

    for i in range(len(nbtfile)):
        if name in nbtfile[i][0]:
            return str(nbtfile[i][1])


def main():
    """
    主函数
    :return:None
    """
    add_w()

    list_mod0 = []  
    list_mod1 = []  
    list_mod2 = []  
    list_mod3 = []
    
    for i in lis:
        nbtfile = nbt.NBTFile(i, 'rb')
        
        nbtfile = str(nbtfile)[1:-1].replace(' ', '').replace('{', '').replace('}', '').replace('[', '').replace(']','').split(',')

        for ii in range(len(nbtfile)):
            nbtfile[ii] = nbtfile[ii].split(':')
        
        a = dat('playerGameType', nbtfile)

        if a == '0':
            list_mod0.append(len_uuid(i))
        elif a == '1':
            list_mod1.append(len_uuid(i))
        elif a == '2':
            list_mod2.append(len_uuid(i))
        elif a == '3':
            list_mod3.append(len_uuid(i))

    if prmod == 0:  

        data = {
            '生存': str(len(list_mod0)),
            '创造': str(len(list_mod1)),
            '冒险': str(len(list_mod2)),
            '旁观': str(len(list_mod3)),
        }

    elif prmod == 1:  

        data = {
            '生存' + str(len(list_mod0)): list_mod0,
            '创造' + str(len(list_mod1)): list_mod1,
            '冒险' + str(len(list_mod2)): list_mod2,
            '旁观' + str(len(list_mod3)): list_mod3,
        }

    return data


if __name__ == '__main__':
    updata()
    print('使用须知\n请不要用本程序去检索热文件，若因为使用不当造成的由使用者承担')

    print('0.统计模式\n1.筛查模式')
    a = input('$:')
    
    if a == '0':
        prmod = 0
    elif a == '1':
        prmod = 1
    else:
        print('输入有误，默认统计模式')
        prmod = 0

    print(main())
