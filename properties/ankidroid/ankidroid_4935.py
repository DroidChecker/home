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

    @precondition(
        lambda self: self.device(text="Day theme").exists() and
        self.device(text="Appearance").exists()
        )
    @rule()
    def back_should_navigate_to_last_page(self):
        self.device.press("back")
        time.sleep(1)
        assert self.device(text="Appearance").exists()
        
start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.9alpha29.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4935/random/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/4935.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
