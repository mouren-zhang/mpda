import glob
import python_nbt.nbt as nbt

# 全局变量
list_path = []  # 可用文件列表
list_err = []  # 错误文件列表


def main(name):
    yn = True
    a = 0
    for i in list_path:
        file = eval(str(nbt.read_from_nbt_file(i)))
        if name in str(file):
            yn = False
            a += 1
            uuid = i[:-4].split('\\')[-1]
            print(a, uuid)

    if yn:
        print('没找到')


def get_filename(data_path):
    """
    将文件路径加入到列表,筛选命名有问题的文件
    :param data_path: 文件夹路径
    :return:
    """
    global list_path
    global list_err

    for i in glob.glob(data_path + r'\*.dat'):
        # 验证数据正确,8-4-4-4-12
        a = i[-40:-4].split('-')
        if len(a[0]) == 8 and len(a[4]) == 12:
            list_path.append(i)
        else:
            list_err.append(i)

    print('加载正确数据【{}】条\n疑似错误数据【{}】条'.format(len(list_path), len(list_err)))


if __name__ == '__main__':
    # 文件路径
    data_path = 'playerdata'
    get_filename(data_path)
    while True:
        print('=' * 20)
        print('目前只能找改名成中文名的物品')
        a = input('名称：')

        main(a)
