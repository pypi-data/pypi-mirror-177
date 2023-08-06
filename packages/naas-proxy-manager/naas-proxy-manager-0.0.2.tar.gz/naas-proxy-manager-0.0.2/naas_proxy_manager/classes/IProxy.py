from naas_proxy_manager.classes.ProxyStatus import ProxyStatus

from abc import ABCMeta, abstractmethod


class IProxy(metaclass=ABCMeta):
    ip : str
    port : int
    status : ProxyStatus

    def __init__(self):
        self.ip = None
        self.port = None
        self.status = ProxyStatus.UNDEFINED

    
    @abstractmethod
    def delete(self):
        raise NotImplementedError
    
    @abstractmethod
    def wait_until_running(self):
        raise NotImplementedError

    @abstractmethod
    def wait_until_ready(self):
        raise NotImplementedError

    @abstractmethod
    def wait_until_deleted(self):
        raise NotImplementedError

    @abstractmethod
    def refresh(self):
        raise NotImplementedError