import ast
import json
import os

import yaml

from app.common.config import cfg


# from app.utils.global_boss_util import BossManager


def is_number(value):
    # 检查 value 是否为列表
    if isinstance(value, list):
        return False

    try:
        float(value)
        return True
    except ValueError:
        return False
def update_target_map_in_yaml(yaml_file_path, target_map):
    """
    读取现有的 YAML 文件，并在其中添加或更新 `TargetMap` 的键值对。
    数字类型的值将以数字形式表示，非数字类型的值将以字符串形式表示。
    target_map 是一个字典，包含要添加或更新到 YAML 文件中的键值对。

    :param yaml_file_path: YAML 文件的路径
    :param target_map: 要添加或更新到 YAML 文件中的键值对字典
    """

    # 读取现有的 YAML 文件内容
    with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
        existing_data = yaml.safe_load(yaml_file)

    # 确保顶层存在 "TargetMap" 键
    if "TargetMap" not in existing_data:
        existing_data["TargetMap"] = {}

    # 更新或添加 "TargetMap" 的键值对
    for key, value in target_map.items():
        # 如果值是数字，则将其转换为相应的数字类型
        if isinstance(value, str):
            if value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

        # 添加或更新到 "TargetMap" 中
        existing_data["TargetMap"][key] = value

    # 将更新后的数据转换为 YAML 格式
    yaml_data = yaml.dump(existing_data, allow_unicode=True)

    # 将 YAML 数据保存回文件中
    with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
        yaml_file.write(yaml_data)


def process_target_map_to_yaml(json_file_path, yaml_file_path):
    if not os.path.exists(json_file_path):
        return
    Zone = get_compute_tactic(json_file_path, 'TargetMap', 'Zone')
    Level = get_compute_tactic(json_file_path, 'TargetMap', 'Level')
    if Zone == "旧都列车":
        array = ["外围", "前线", "内部", "腹地", "核心"]
        if not Level:
            return
        find_index = find_index_in_array(Level, array)
        target_map = {
            "Level":1,
            "Zone": find_index
        }
        update_target_map_in_yaml(yaml_file_path, target_map)
    if Zone == "施工废墟":
        array = ["前线", "内部", "腹地", "核心"]
        if not Level:
            return
        find_index = find_index_in_array(Level, array)
        target_map = {
            "Level": 2,
            "Zone": find_index
        }
        update_target_map_in_yaml(yaml_file_path, target_map)

def get_config_value(config_path, key):
    """
    从指定的 YAML 配置文件中获取给定键的值。

    :param config_path: 配置文件的路径
    :param key: 要获取的键
    :return: 键对应的值，如果键不存在则返回 None
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get(key)  # 使用 get 方法，如果键不存在则返回 None
    except FileNotFoundError:
        # print(f"配置文件 {config_path} 未找到")
        return None
    except Exception as e:
        # print(f"读取配置文件时发生错误: {e}")
        return None


def append_array_to_yaml(yaml_file_path: str, key: str, array: list):
    """
    将指定的键和数组值追加到YAML配置文件中。

    参数:
    - yaml_file_path (str): YAML配置文件的路径。
    - key (str): 需要追加的键。
    - array (list): 需要追加的数组。

    返回值:
    None
    """

    # 尝试读取YAML文件中的现有内容
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
            existing_data = yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        existing_data = {}

    # 将键和数组值添加到现有数据中
    existing_data[key] = array

    # 将更新后的数据写入到YAML文件中
    try:
        with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(existing_data, yaml_file, allow_unicode=True)
    except Exception as e:
        print(f"Error writing to YAML file: {e}")


def delete_keys_from_yaml(yaml_file_path: str, keys: list):
    """
    从YAML配置文件中删除多个指定的键和值。

    参数:
    - yaml_file_path (str): YAML配置文件的路径。
    - keys (list): 需要删除的键的列表。

    返回值:
    None
    """

    # 从YAML文件中读取数据
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return

    # 遍历需要处理的键列表
    for key in keys:
        # 检查键是否存在于YAML数据字典中
        if key in yaml_data:
            # 如果存在，删除该键值对
            del yaml_data[key]

    # 将更新后的YAML数据写回YAML文件中
    try:
        with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(yaml_data, yaml_file, allow_unicode=True)
    except Exception as e:
        print(f"Error writing to YAML file: {e}")


def append_array_from_json_to_yaml(json_file_path: str, yaml_file_path: str, key: str):
    # 检查字符串类型 '[10,20,30]' 是否是1个数组
    """
    从JSON配置文件中读取特定键的值，如果该值是一个数组，
    则以数组的形式追加到YAML配置文件中。

    参数:
    - json_file_path (str): JSON配置文件的路径。
    - yaml_file_path (str): YAML配置文件的路径。
    - key (str): 需要读取的键。

    返回值:
    None
    """

    # 尝试读取JSON文件中的现有内容
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # 检查特定键的值是否是一个数组
    if key in json_data and isinstance(json_data[key], list):
        # 如果值是一个数组，读取YAML文件中的现有内容
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
                existing_data = yaml.safe_load(yaml_file)
        except Exception as e:
            print(f"Error reading YAML file: {e}")
            existing_data = {}

        # 将数组值添加到现有数据中
        existing_data[key] = json_data[key]

        # 将更新后的数据写入到YAML文件中
        try:
            with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(existing_data, yaml_file, allow_unicode=True)
        except Exception as e:
            print(f"Error writing to YAML file: {e}")
    else:
        print(f"Key '{key}' not found in JSON file or value is not a list.")


def extract_values_from_yaml(yaml_file_path: str, keys: list) -> list:
    """
    从YAML配置文件中提取多个指定键的值，并将这些值作为字符串保存在列表中。

    参数:
    - yaml_file_path (str): YAML配置文件的路径。
    - keys (list): 需要提取的键的列表。

    返回值:
    list: 包含指定键值（作为字符串）的列表。
    """

    # 初始化一个空列表来存储找到的值
    values = []

    # 从YAML文件中读取数据
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return values

    # 遍历需要处理的键列表
    for key in keys:
        # 检查键是否存在于YAML数据字典中
        if key in yaml_data:
            # 检查键的值是否为空
            if yaml_data[key] is not None and yaml_data[key] != '无  (跳过)':
                # 如果存在，将值转换为字符串并添加到列表中
                values.append(str(yaml_data[key]))

    return values


def replace_value_in_yaml(yaml_file_path: str, key: str, new_value):
    """
    在YAML配置文件中替换特定键的值，同时保留其他内容不变。

    参数:
    - yaml_file_path (str): YAML配置文件的路径。
    - key (str): 需要替换的键。
    - new_value: 新的值。

    返回值:
    None
    """

    # 尝试读取YAML文件中的现有内容
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
            data = yaml.safe_load(yaml_file)
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return

    # 使用递归函数来深入嵌套字典并替换键的值
    def update_dict(d, target_key, value):
        for k, v in d.items():
            if k == target_key:
                d[k] = value
            elif isinstance(v, dict):
                update_dict(v, target_key, value)

    # 替换键的值
    update_dict(data, key, new_value)

    # 将更新后的数据写入到YAML文件中
    try:
        with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(data, yaml_file, allow_unicode=True)
    except Exception as e:
        print(f"Error writing to YAML file: {e}")


def get_compute_tactic(json_file_path: str, groupName, keyName):
    """
    从JSON配置文件中读取ComputeTactic的值。

    参数:
    - json_file_path (str): JSON配置文件的路径。

    返回值:
    str or list: ComputeTactic的值，可能是字符串或列表。
    """
    # 检查文件是否存在
    if not os.path.exists(json_file_path):
        # print(f"文件 {json_file_path} 不存在，请检查路径。")
        # 如果文件不存在，如果直接返回None，在使用os.path.join方法的时候会报错，所以返回字符串"None"
        return None

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            compute_tactic = data.get(groupName, {}).get(keyName)
            return compute_tactic
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


def update_config_value(json_file_path, groupName, keyName, newValue):
    """
    更新JSON配置文件中指定组的指定键的值。

    参数:
    json_file_path: 字符串，表示JSON配置文件的路径。
    groupName: 字符串，表示要更新的组名。
    keyName: 字符串，表示要更新的键名。
    newValue: 新的值，更新配置文件中指定键的值。

    抛出:
    ValueError: 如果指定的组不存在或不是字典类型，则抛出此异常。

    更新配置文件中指定组的指定键的值，如果组或键不存在，则抛出异常。
    """
    # 加载JSON配置文件
    # 读取现有的配置文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        config_data = json.load(file)

    # 检查指定的组是否存在且为字典类型，然后更新键的值
    # 更新groupName下的keyName的值
    if groupName in config_data and isinstance(config_data[groupName], dict):
        config_data[groupName][keyName] = newValue
    # else:
    #     raise ValueError(f"Group '{groupName}' not found or not a dictionary.")

    # 将更新后的配置数据写回配置文件
    # 将更新后的配置写回文件
    with open(json_file_path, 'w') as file:
        json.dump(config_data, file, indent=4)


def process_key_boss__to_array(yaml_file_path, key1, key2, key3, key_name):
    # =============================================================
    # 处理Boos部分，确保保存在config.yaml中的值是数组形式
    # 得到Boss的名称，并将其保存到数组中
    keys = [key1, key2, key3]
    values = extract_values_from_yaml(yaml_file_path, keys)

    # 将指定的多个键，删除从config.yaml删除掉
    delete_keys_from_yaml(yaml_file_path, keys)
    # 指定键和值写入到config.yaml中
    append_array_to_yaml(yaml_file_path, key_name, values)
    # =============================================================


def update_yaml_file(file_path, key_name, new_value):
    """
    更新或添加YAML文件中的键值对。

    参数:
    file_path (str): YAML文件的路径。
    key_name (str): 要更新或添加的键名。
    new_value (any): 关联到键名的新值。

    返回:
    None
    """

    # 读取现有的YAML文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file) or {}

    # 检查键名是否已经存在于YAML文件中
    if key_name in data:
        # 如果存在，更新该键的值
        data[key_name] = new_value
    else:
        # 如果不存在，添加新的键值对
        data[key_name] = new_value

    # 写回更新后的内容到YAML文件
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file, allow_unicode=True)








def process_input_keys_to_arrays(groupName, keyName, config_yaml_path, config_json_path):
    # 处理输入的键是字符串格式。并且是一个数组  ’[1,2,3]‘
    # 得到AcousticSynthesisComputer组中ComputeTactic的值
    computeTactic_value = get_compute_tactic(config_json_path, groupName, keyName)
    # 尝试将array转为python对象
    try:
        array = json.loads(computeTactic_value)
        if isinstance(array, list):  # 如果值是数组
            update_yaml_file(config_yaml_path, keyName, array)
    except Exception as e:
        print(f"Error parsing array: {e}")


def process_path(groupName, keyName, config_yaml_path, json_path):
    # 得到AcousticSynthesisComputer组中ComputeTactic的值
    app_path = get_compute_tactic(json_path, groupName, keyName)
    # 将路径中的所有 / 替换为 \\
    app_path = app_path.replace('/', '\\\\')
    # 重新替换掉config.yaml文件中的app_path的值
    update_yaml_file(config_yaml_path, keyName, app_path)  # 键存在，替换值，键不存在,新建键和值





def find_index_in_array(value, array):
    """
    查找给定值在数组中的索引位置。

    :param value: 要查找的值
    :param array: 数组
    :return: 如果找到值，则返回其在数组中的索引；否则返回-1
    """
    try:
        index = array.index(value)
        return index + 1
    except ValueError:
        return -1


def process_mode_select(yaml_file_path, json_file_path):
    global base_path
    if not os.path.exists(json_file_path):
        return
    # 处理modeSelect属性
    modeSelect = get_compute_tactic(json_file_path, 'AutoBattle', 'ModeSelect')
    find_index = find_index_in_array(modeSelect, ['全通关', '零号业绩', '零号银行', '业绩与银行'])
    if find_index != -1:
        update_yaml_file(yaml_file_path, 'ModeSelect', find_index)





# 生成config.yaml
# 主调用
def convert_sections_to_yaml(json_file_path, yaml_file_path, section_names, exclude_keys):
    """
    从指定的JSON文件读取多个指定部分，并将它们合并后转换为YAML格式，保存到指定的YAML文件中。
    数字类型的值将以数字形式表示，非数字类型的值将以字符串形式表示。
    exclude_keys 是一个数组，包含不应该添加到 YAML 文件中的键。

    :param json_file_path: 包含指定部分的JSON文件路径
    :param yaml_file_path: 输出YAML文件的路径
    :param section_names: 要提取和转换的JSON部分的键名列表
    :param exclude_keys: 不应该添加到 YAML 文件中的键的列表
    """
    if not os.path.exists(json_file_path):
        return
    # 从文件中读取JSON数据
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    # 创建一个字典来存储最终的YAML数据
    final_yaml_data = {}

    # 遍历每个指定的部分
    for section_name in section_names:
        # 获取指定部分
        section_config = data_dict.get(section_name, {})

        # 将每个部分内的键值对添加到最终的YAML数据中
        for key, value in section_config.items():
            # 检查是否应该排除此键
            if key in exclude_keys:
                continue

            # 如果值是数字，则将其转换为相应的数字类型
            if is_number(value):
                if isinstance(value, str):
                    value = int(value) if value.isdigit() else float(value)

            # 直接添加到最终的YAML数据中
            final_yaml_data[key] = value

    # 将合并后的数据转换为YAML格式
    yaml_data = yaml.dump(final_yaml_data, allow_unicode=True)

    # 将YAML数据保存到文件中
    with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
        yaml_file.write(yaml_data)


# 组名作为yaml的顶级键，键和值作为yaml的字典
def convert_grounpname_to_yaml(json_file_path, yaml_file_path, section_names):
    """
    从指定的JSON文件读取多个指定部分，并将它们合并后转换为YAML格式，保存到指定的YAML文件中。
    数字类型的值将以数字形式表示，非数字类型的值将以字符串形式表示。

    :param json_file_path: 包含指定部分的JSON文件路径
    :param yaml_file_path: 输出YAML文件的路径
    :param section_names: 要提取和转换的JSON部分的键名列表
    """
    # 从文件中读取JSON数据
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    # 创建一个字典来存储最终的YAML数据
    final_yaml_data = {}

    # 遍历每个指定的部分
    for section_name in section_names:
        # 获取指定部分
        section_config = data_dict.get(section_name, {})

        # 创建一个字典来存储当前组名下的键值对
        section_yaml_data = {}

        # 将每个部分内的键值对添加到当前组名下的字典中
        for key, value in section_config.items():

            # 如果值是数字，则将其转换为相应的数字类型
            if is_number(value):
                if isinstance(value, str):
                    value = int(value) if value.isdigit() else float(value)

            # 添加到当前组名下的字典中
            section_yaml_data[key] = value

        # 将当前组名下的字典添加到最终的YAML数据中
        final_yaml_data[section_name] = section_yaml_data

    # 将合并后的数据转换为YAML格式
    yaml_data = yaml.dump(final_yaml_data, allow_unicode=True)

    # 将YAML数据保存到文件中
    with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
        yaml_file.write(yaml_data)


# 当前项目根目录(GUI）
base_path = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# config.json
json_file_path = os.path.join(base_path, "AppData", "config.json")  # 替换为实际的JSON文件路径


# 生成config.yaml

def generateConfigFile():
    global project_root
    global base_path
    global json_file_path
    # 获取项目根目录(脚本)
    project_root = get_compute_tactic(json_file_path, 'AutoBattle', 'ProjectRootPath')
    if project_root is None:  # 如果config.json中没有配置项目根目录，则使用当前项目根目录
        project_root = base_path
    yaml_file_path = project_root + '\\' + 'config.yaml'  # 生成config.yaml路径
    # todo...从config.json中提取出【组部分】的属性键和值，生成config.yaml文件
    section_names = ['AutoBattle']  # 指定组名下的属性键和值
    en_include = ['ProjectRootPath', 'modelSelect']  # 需要排除的添加的键
    convert_sections_to_yaml(json_file_path, yaml_file_path, section_names, en_include)
    # todo...处理modeSelect属性
    process_mode_select(yaml_file_path, json_file_path)
    # todo...处理TargetMap组中的Level与Zone属性
    process_target_map_to_yaml(json_file_path, yaml_file_path)

generateConfigFile()


def is_write_config_yaml():
    project_root = get_compute_tactic(json_file_path, 'AutoBattle', 'ProjectRootPath')
    if project_root is None:  # 从配置config.json中获取不到项目根目录，则使用默认的指定的路径
        project_root = base_path
    echo_config_yaml_path = project_root + '\\' + 'config.yaml'
    return True if os.path.exists(echo_config_yaml_path) else False







