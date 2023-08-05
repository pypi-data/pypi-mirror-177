from pprint import pprint


# 逐行打印内容
def fprint(*args):
    for arg in args:
        if type(arg) in [int, float, str]:
            print(arg)
        else:
            pprint(arg)
    print('')
