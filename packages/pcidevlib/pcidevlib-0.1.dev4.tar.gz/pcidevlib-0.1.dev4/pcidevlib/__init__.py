# UNDER DEVELOPMNENT
import os
import logging
import pathlib

def module_logger(name):
    """
    Package logger
    """
    formatter = logging.Formatter(fmt='[%(asctime)s] ** %(levelname)s ** %(module)s: %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

class Meta():
    """
    Meta information about the package.
    """

    def __init__(self):
        self.__meta_path    = pathlib.PosixPath(os.path.dirname(__file__) + "/meta")
        self.__version      = (self.__meta_path / "version").read_text(encoding="utf-8")
        self.__pname        = (self.__meta_path / "pname").read_text(encoding="utf-8")
        self.__description  = (self.__meta_path / "description").read_text(encoding="utf-8")
    
    def version(self):
        return self.__version
    
    def pname(self):
        return self.__pname
    
    def description(self):
        return self.__description

# INSTANTIATE
__log = module_logger(Meta().pname())

if __name__ == "__main__":
    __log.warning('DO NOT RUN PCIDEVLIB AS MAIN')
    pass
