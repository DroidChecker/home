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
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)
    # 1920
    @precondition(lambda self: self.device(text="FTP Server").exists() and self.device(text="START").exists())
    @rule()
    def should_notice_user_when_no_network(self):
        self.device(text="START").click()
        time.sleep(1)
        assert self.device(text="STOP").exists()

start_time = time.time()


t = Test(
    apk_path="./apk/amaze/3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1920/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
