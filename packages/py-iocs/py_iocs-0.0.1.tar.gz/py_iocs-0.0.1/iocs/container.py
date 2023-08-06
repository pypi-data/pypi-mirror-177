class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class Initializer(object):
    """
    初始化器类，保持初始化的构造器信息
    """
    def __init__(self, cls, init_method, is_single: bool):
        self.cls = cls
        self.method = init_method
        self.is_single = is_single


@Singleton
class IocContainer(object):
    """
    先保持自己是一个单利
    """
    def __init__(self):
        self.dependencies = {}
        self.single_instances = {}
        self.initializers = {}

    def regist_classes(self, cls, initial_method, is_single: bool = False):
        """
        注册需要注入的类
        :param is_single: 是否是单例
        :param cls: 注入的类
        :param initial_method: 实例化函数
        :return:
        """
        self.initializers[cls] = Initializer(cls, initial_method, is_single)

    def __call__(self, cls):
        """
        获取实例
        :param cls:
        :return:
        """
        assert cls in self.initializers
        ins: Initializer = self.initializers.get(cls)
        if ins.is_single:
            instance = self.single_instances.get(cls)
            if instance:
                return instance
        return ins.method(self.dependencies)

    def update_dependencies(self, **dependencies):
        """
        更新要注入实例的依赖项目
        :param dependencies:
        :return:
        """
        self.dependencies.update(dependencies)

