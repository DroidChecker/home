import string
from main import *
import time
import sys
import re

class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
        main_path=None
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
            main_path=main_path
        )

    @initialize()
    def set_up(self):
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        
    
    # bug #457
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/nav_notebook").exists())
    @rule()
    def swipe_should_update_title(self):
        # self.device.swipe_ext("left")
        if self.device(resourceId="net.gsantner.markor:id/nav_todo").info["selected"]:
            assert  self.device(resourceId="net.gsantner.markor:id/toolbar").child(text="To-Do").exists(), "To-Do not exists"
        elif self.device(resourceId="net.gsantner.markor:id/nav_quicknote").info["selected"]:
            assert  self.device(resourceId="net.gsantner.markor:id/toolbar").child(text="QuickNote").exists(), "QuickNote not exists"
        elif self.device(resourceId="net.gsantner.markor:id/nav_more").info["selected"]:
            assert  self.device(resourceId="net.gsantner.markor:id/toolbar").child(text="More").exists(),   "More not exists"


start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/457/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/457_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
