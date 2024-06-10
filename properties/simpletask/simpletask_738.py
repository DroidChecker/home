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
        lambda self: self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").exists() and 
        self.device(resourceId="nl.mpcjanssen.simpletask:id/search").exists() and not 
        self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not 
        self.device(text="Quick filter").exists() and not 
        self.device(text="Settings").exists() and not 
        self.device(text="Saved filters").exists()
    )
    @rule()
    def click_new_task_should_enter_add_task_instead_of_update(self):
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        time.sleep(1)
        assert self.device(text="Add Task").exists(), "Add Task should exist"
       
start_time = time.time()

t = Test(
    apk_path="./apk/simpletask/9.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/738/random_100/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/simpletask/738.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
