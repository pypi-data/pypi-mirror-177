from naas_proxy_manager.classes.IProxyType import IProxyType
from naas_proxy_manager.classes.IProxy import IProxy
from naas_proxy_manager.classes.ProxyType import ProxyType

from naas_proxy_manager.classes.Provider import Provider

from typing import List
from abc import ABCMeta, abstractmethod

class IProxyProvider(metaclass=ABCMeta):

    provider : Provider
    proxy_types : IProxyType
    proxies : List[IProxy]

    @abstractmethod
    def list_proxies(self) -> list:
        raise NotImplementedError
    
    @abstractmethod
    def describe_proxy(self, proxy_id: str) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    def create_proxy(self, proxy_type:IProxyType, params:dict = {}) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    def delete_proxy(self, proxy_id: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def delete_all_proxies(self) -> None:
        raise NotImplementedError

    def implements_proxy_type(self, proxy_type:ProxyType) -> bool:
        return proxy_type in list(i.name for i in self.proxy_types)
