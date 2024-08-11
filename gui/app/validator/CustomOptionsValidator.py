from enum import Enum
from qfluentwidgets import ConfigValidator


class CustomOptionsValidator(ConfigValidator):
    """
    选项验证器类，继承自ConfigValidator。

    该类用于验证一个值是否在一组选项中。
    初始化时接受一个options参数，可以是集合或枚举类型。
    如果传入的是枚举类型，它会被转换为枚举值的列表。

    属性:
        options (list): 所有可能选项的列表。
    """

    def __init__(self, options):

        # 检查`options`参数是否为空，确保后续操作可以顺利进行
        if not options:
            raise ValueError("参数 `options` 不能为空。")

        # 如果`options`是枚举类型，将其转换为枚举成员的值的列表
        # 这样做是为了统一处理不同类型的`options`参数，确保后续可以无差别地处理
        if isinstance(options, Enum):
            options = options._member_map_.values()

        # 将`options`转换为列表形式并赋值给`self.options`
        # 这一步确保了`self.options`始终是列表类型，提高了代码的健壮性和可用性
        self.options = list(options)

    def validate(self, value):
        """
        验证给定的值是否在options列表中。

        参数:
            value: 待验证的值。

        返回:
            bool: 如果value存在于options列表中则返回True，否则返回False。
        """
        return value in self.options

    def correct(self, value):
        """
        校正给定的值，如果该值不在options列表中，则返回列表中的第一个元素作为默认值。

        参数:
            value: 待校正的值。

        返回:
            任何类型: 如果value存在于options列表中则返回value本身，否则返回options列表的第一个元素。
        """
        return value if self.validate(value) else self.options[0]
