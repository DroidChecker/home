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
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @initialize()
    def set_up(self):
        pass

    @precondition(
        lambda self: self.device(text="Preview").exists() and self.device(text="SHOW ANSWER").exists()
    )
    @rule()
    def show_answer_button_should_only_display_one(self):
        assert self.device(text="SHOW ANSWER").count == 1, "SHOW ANSWER button should only display one"
        
start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.13alpha26.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7027/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
