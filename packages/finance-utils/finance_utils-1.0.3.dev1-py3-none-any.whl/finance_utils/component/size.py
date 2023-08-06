# 计算画布中的最佳尺寸
def get_size_param(figsize: tuple):
    '''
    根据绘图的画布尺寸，计算参数的尺寸
    
    :param figsize:
    :return:尺寸参数字典
    '''
    text_fontsize = int(15 / 20 * figsize[0])
    line_width = round((max(figsize[0] / 20, 1)), 2)
    point_size = round(max(figsize[0] / 20 * 100, 100), 2)
    ticks_fontsize = int(10 * figsize[0] / 20)
    label_fontsize = int(15 * figsize[0] / 20)
    title_fontsize = int(15 * figsize[0] / 20)
    return locals()


if __name__ == '__main__':
    print(get_size_param(figsize=(25, 8)))
