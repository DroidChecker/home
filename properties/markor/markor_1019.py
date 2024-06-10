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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        time.sleep(1)
    
    @precondition(
        lambda self: 
        self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__description").exists() and 
        self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__description").get_text() != "/storage/emulated/0/Documents"
        )
    @rule()
    def rotate_device_should_not_change_the_title(self):
        title = self.device(resourceId="net.gsantner.markor:id/toolbar").child(className="android.widget.TextView").get_text()
        print("title: "+str(title))
        assert title != "markor", "title should not be markor"

start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1019/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/1019.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
