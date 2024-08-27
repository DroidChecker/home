from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device
import time
from typing import Any, Union

class Mobile(Device):
    
    def __init__(self, delay=1) -> None:
        
        self.delay = delay

    def set_device_serial(self, serial):
        super().__init__(serial=serial)

    def __call__(self, **kwargs: Any) -> Any:
        return Ui(self, Selector(**kwargs))

    def set_droidbot(self, droidbot):
        self.droidbot = droidbot

    def rotate(self, mode: str):
        super().set_orientation(mode)
        time.sleep(self.delay)
        self.droidbot.device.take_screenshot(True, "rotate")

    def press(self, key: Union[int, str], meta=None):
        super().press(key, meta)
        time.sleep(self.delay)
        self.droidbot.device.take_screenshot(True, "press")


class Ui(UiObject):

    def click(self, timeout=None, offset=None):
        super().click(timeout, offset)
        time.sleep(self.session.delay)
        self.session.droidbot.device.take_screenshot(True, "click")

    def long_click(self, duration: float = 0.5, timeout=None):
        super().long_click(duration, timeout)
        time.sleep(self.session.delay)
        self.session.droidbot.device.take_screenshot(True, "long_click")
    
    def set_text(self, text, timeout=None):
        super().set_text(text, timeout)
        time.sleep(self.session.delay)
        self.session.droidbot.device.take_screenshot(True, "set_text "+text)
        
    def child(self, **kwargs):
        return Ui(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs))