import json
import copy


def toDict(obj):
    """ serialize a class into dict
    for complex type, the class should implement toDict method

    """

    if hasattr(obj, "toDict") and callable(getattr(obj, "toDict")):
        return obj.toDict()
    else:
        result = copy.copy(obj.__dict__)

        for k,v in obj.__dict__.items():
            if hasattr(v, '__dict__'):
                result[k] = toDict(v)

        return result

def loadDict(obj, d, allowMissing=False):
    """ deserialize a dict back to the class.
    for complex type, the class should implement loadDIct method
    Parameters:
        d - the dict for deserializing
        obj - the prototype for deserializing
    """
    if hasattr(obj, "loadDict") and callable(getattr(obj, "loadDict")):
        obj.loadDict(d, allowMissing=allowMissing)
    else:
        if isinstance(obj, dict):
            targetDict = obj
        else:
            targetDict = obj.__dict__

        for k in targetDict:
            if allowMissing and k not in d:
                continue

            if hasattr(targetDict[k], '__dict__'):
                loadDict(targetDict[k], d[k], allowMissing= allowMissing)
            else:
                targetDict[k] = copy.deepcopy(d[k])

    return obj


def importModule(name):
    import importlib
    return importlib.import_module(name)


def recursiveGetAttr(obj, name):
    components = name.split('.')
    for comp in components:
        obj = getattr(obj, comp)
    return obj

class ModuleConf:
    def __init__(self, config=None, module=None, moduleName=None, configClassName=None):
        self.config = config
        self.module = module
        self.moduleName = moduleName
        self.configClassName = configClassName

    def toDict(self):
        return {
                "module": self.moduleName,
                "configClassName": self.configClassName,
                "config": toDict(self.config)
                }

    def loadDict(self, d, allowMissing=False):
        self.__dict__.update(makeModuleConf(d["module"], d["configClassName"]).__dict__)
        loadDict(self.config, d["config"], allowMissing= allowMissing)



def makeModuleConf(moduleName, configClassName= "Config"):

    module = importModule(moduleName)
    Config = recursiveGetAttr(module, configClassName)
    config = Config()

    return ModuleConf(config, module, moduleName, configClassName)


def parse(s, allowMissing = False):
    # get all keys
    result = {k: ModuleConf() for k in s}
    loadDict(result, s, allowMissing)
    return result

def parseFromString(inputStr, allowMissing= False):
    return parse(json.loads(inputStr), allowMissing)


def parseFromFile(filepath, allowMissing = False):
    with open(filepath, 'r') as f:
        conf = parse(json.load(f))
    
    return conf

