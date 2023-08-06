from _typeshed import Incomplete
from abc import ABCMeta
from collections import UserList
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By as By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from typing import List, Optional

class PageMeta(ABCMeta):
    driver: WebDriver
    wait: WebDriverWait
    time_out: float
    poll: float
    url: str
    def __new__(cls, *args, **kwargs): ...

class BaseLazy(metaclass=ABCMeta):
    driver: Optional[WebDriver]
    def __getattribute__(self, item: str): ...
    def update(self, **kwargs) -> None: ...
    @classmethod
    def from_instance(cls, obj): ...

class LazyElement(BaseLazy, WebElement):
    obj_list: Optional[List[WebElement]]
    by: Incomplete
    value: Incomplete
    check_on_init: Incomplete
    time_out: Incomplete
    poll: Incomplete
    def __init__(self, by, value, check_on_init: bool = ..., time_out: Incomplete | None = ..., poll: Incomplete | None = ..., *args, **kwargs) -> None: ...

class LazyElementList(LazyElement, UserList):
    def __new__(cls, *args, **kwargs) -> UserList[WebElement]: ...
    def __len__(self): ...
    def __getitem__(self, index): ...
    def __iter__(self): ...

class LazyAlert(BaseLazy, Alert):
    check_on_init: Incomplete
    time_out: Incomplete
    poll: Incomplete
    def __init__(self, check_on_init: bool = ..., time_out: Incomplete | None = ..., poll: Incomplete | None = ...) -> None: ...

class BasePage(metaclass=PageMeta):
    url: str
    time_out: int
    poll: float
    alert: Incomplete
    driver: Incomplete
    wait: Incomplete
    def __init__(self, driver: WebDriver) -> None: ...
    @classmethod
    def start(cls, driver, *args, **kwargs): ...
    def click(self, ele: LazyElement, by_js: bool = ...): ...
    def send_keys(self, ele: LazyElement, content: str = ..., clear: bool = ..., by_js: bool = ...): ...
    def upload(self, ele: LazyElement, file_path, drop: bool = ...): ...
    def wait_url_change(self) -> None: ...
    def select(self, ele: LazyElement, value: str) -> Optional[Select]: ...
    def chosen(self, ele: LazyElement, value: str): ...

class AlertPage(BasePage):
    def ok(self, content: Incomplete | None = ...) -> None: ...
    def cancel(self) -> None: ...
