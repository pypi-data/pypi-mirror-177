import json
import os
from tdf_tools.tools.gitlab.gitlab_utils import GitlabUtils
from tdf_tools.tools.print import Print
from tdf_tools.tools.shell_dir import ShellDir


class ModuleTools:
    # 获取项目初始化数据
    def getInitJsonData():
        ShellDir.goTdfCacheDir()
        ModuleTools.sureInitialConfigFile()
        with open(".initial_config.json", "r", encoding="utf-8") as readF:
            fileData = readF.read()
            readF.close()
            return json.loads(fileData)

    def getModuleNameList():
        initJsonData = ModuleTools.getInitJsonData()
        if initJsonData.__contains__("moduleNameList") and isinstance(
            initJsonData["moduleNameList"], list
        ):
            moduleNameList = initJsonData["moduleNameList"]
            return moduleNameList
        else:
            Print.error("❌ 请配置moduleNameList的值,以数组形式")

    def getModuleJsonData():  # 获取模块 git相关配置信息
        ShellDir.goTdfCacheDir()
        with open("module_config.json", "r", encoding="utf-8") as readF:
            fileData = readF.read()
            readF.close()
            return json.loads(fileData)

    # 确保initial_config文件存在
    def sureInitialConfigFile():
        if os.path.exists(".initial_config.json"):
            os.remove(".initial_config.json")

        gitlabUtils = GitlabUtils()
        curBranch = gitlabUtils.getCurBranch()

        ShellDir.goInShellDir()
        shellModule = os.path.dirname(
            os.path.abspath(__file__)).split('/').pop()

        moduleJson = ModuleTools.getModuleJsonData()
        sourceModuleList = []
        for item in moduleJson:
            # 读取所有打开源码开关的模块
            if moduleJson[item].__contains__('importSource') and moduleJson[item]['importSource'] == True:
                sourceModuleList.append(item)

        with open(".initial_config.json", "w", encoding="utf-8") as wf:
            initialDic = dict()
            initialDic["featureBranch"] = curBranch
            initialDic["shellName"] = shellModule
            initialDic["moduleNameList"] = sourceModuleList
            wf.write(json.dumps(initialDic, indent=2))
            wf.close()
