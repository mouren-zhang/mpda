import glob
from nbt import nbt


def main():
    lis = []

    for filename in glob.glob(r'playerdata\*.dat'):
        lis.append(filename)

    for i in lis:
        if len(i[11:]) > 41:
            print('疑似错误文件', i[11:])
            continue

        nbtfile = nbt.NBTFile(i, 'rb')

        # 0为生存模式，1为创造模式，2为冒险模式，3为旁观模式。
        
        txt = "TAG_Int('playerGameType'): 1"

        if txt in str(nbtfile):
            print('创造模式：',i)


if __name__ == '__main__':
    main()
