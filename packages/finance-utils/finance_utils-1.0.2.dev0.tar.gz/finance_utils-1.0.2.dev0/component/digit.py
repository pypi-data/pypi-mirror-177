# 保存源字符串的浮点数
class digit_float(float):
    def __init__(self, text: str):
        self.__text = text

    def orgin(self):
        return self.__text


# 保存源字符串的整数
class digit_int(int):
    def __init__(self, text: str):
        self.__text = text

    def orgin(self):
        return self.__text
