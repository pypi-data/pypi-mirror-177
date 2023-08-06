import random


def add(a, b):
    """
    两数相加
    """
    return a + b


def sub(a, b):
    """
    两数相减
    """
    return a - b


def mul(a, b):
    """
    两数相乘
    """
    return a * b


def div(a, b):
    """
    两数相除
    """
    return a / b


def rl1n_to_l2(l1, l2, n=0):
    """
    从列表1的n坐标处拼接列表2,默认从0坐标处替换
    """
    return l1[:n] + l2


def flatten_list(l):
    """
    返回拉平的多维数组
    """
    return sum(l, [])


def random_list_n(al, n):
    """
    从源数组的值中随机分配出不重复的包含源数组值n个数组
    al: 源数组
    n: 这个月这个人参与的项目
    """
    result = [[] for _ in range(n)]
    while len(flatten_list(result)) < len(al):
        tmp_work = flatten_list(result)
        # 从源数组中取值
        yidx = random.randint(0, len(al) - 1)
        # 从分配的数组中挑出要存入值的数组
        nidx = random.randint(0, n - 1)
        z = al[yidx]
        # 判断当前值是不是已经用过了
        if z in tmp_work:
            continue
        result[nidx].append(z)

    return result
