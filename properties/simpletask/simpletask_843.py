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
        lambda self: self.device(text="Add Task").exists() and 
        len(self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text())!=121
    )
    @rule()
    def rotate_device_should_keep_text(self):
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        self.device.set_orientation("l")
        time.sleep(1)
        self.device.set_orientation("n")
        time.sleep(1)
        new_content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("new content: "+str(new_content))
        assert content == new_content

        
start_time = time.time()

t = Test(
    apk_path="./apk/simpletask/10.0.7.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/843/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/simpletask/843.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
