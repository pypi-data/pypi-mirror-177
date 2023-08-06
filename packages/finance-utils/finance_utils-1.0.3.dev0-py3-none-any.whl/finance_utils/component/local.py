# 函数中的局部变量变成字典
def to_local(data: dict, filter_keys=['self', '__class__']):
    local_data = {}
    for k, v in data.items():
        if k not in filter_keys:
            local_data[k] = v
    return local_data
