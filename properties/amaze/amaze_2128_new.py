import string
import sys
import time
sys.path.append("..")
from main import *

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
        if self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)
        if self.device(text="GRANT").exists():
            self.device(text="GRANT").click()

    # 2128
    @precondition(lambda self:  self.device(text="Amaze").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/fullpath").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/item_count").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/search").exists() and not
                  self.device(resourceId="com.amaze.filemanager:id/search_edit_text").exists() and 
                  "/" in self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text() 
                  ) 
    @rule()
    def rule_FAB_should_appear(self):
        print("time: " + str(time.time() - start_time))
        assert self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists(), "FAB should appear"

    

start_time = time.time()


t = Test(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2128/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/2128_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
