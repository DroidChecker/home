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
        if self.device(text="GRANT").exists():
            self.device(text="GRANT").click()
            time.sleep(1)
        elif self.device(text="Grant").exists():
            self.device(text="Grant").click()
            time.sleep(1)

        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)

    @precondition(lambda self: self.device(text="App Manager").exists() and self.device(description="More options").exists() and not self.device(text="Settings").exists())
    @rule()
    def click_exist_button_should_work(self):
        print("time: " + str(time.time() - start_time))
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Exit").click()
        time.sleep(1)
        assert not self.device(text="App Manager").exists()
    

start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-9f3f1dc6c3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2518/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/2518.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
