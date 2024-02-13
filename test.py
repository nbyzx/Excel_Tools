def run_before(func):
    def wrapper(self, *args, **kwargs):
        # 在执行函数之前执行其他操作
        print("在执行函数之前执行其他操作")
        # 修改 self.name 的值
        self.name = "新的值"
        # 执行原始函数
        return func(self, *args, **kwargs)

    return wrapper


class MyClass:
    def __init__(self):
        self.name = None

    @run_before
    def my_function(self):
        print(self.name)
        print("执行我的函数")


# 创建类的实例
obj = MyClass()
# 调用类函数
obj.my_function()
