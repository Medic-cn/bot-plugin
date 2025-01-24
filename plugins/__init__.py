import os
import glob
import importlib

# 存储插件名和类的字典
plugins = {}

# 获取当前文件夹下的所有 .py 文件（排除 __init__.py）
module_files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for file in module_files:
    module_name, ext = os.path.splitext(os.path.basename(file))
    if module_name != "__init__" and ext == ".py":
        # 动态加载模块
        module = importlib.import_module(f".{module_name}", package=__name__)
        
        # 检查是否有 P_NAME 和类
        if hasattr(module, "P_NAME"):
            p_name = getattr(module, "P_NAME")  # 获取 P_NAME
            # 查找模块中的类（与 P_NAME 相同的类名）
            if hasattr(module, "Main"):
                plugin_class = getattr(module, "Main")
                plugins[p_name] = plugin_class  # 注册到字典中
