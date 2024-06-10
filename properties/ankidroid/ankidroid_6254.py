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
        if self.device(text="OK").exists():
            self.device(text="OK").click()

    @precondition(
        lambda self: self.device(text="Language").exists() and 
        self.device(text="AnkiDroid").exists() 
    )
    @rule()
    def yue_should_display_in_language(self):
        self.device(text="Language").click()
        time.sleep(1)
        assert self.device(scrollable=True).scroll.to(text="yue")

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.11alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6254/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/6254.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
