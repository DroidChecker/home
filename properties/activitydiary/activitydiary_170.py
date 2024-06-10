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
        lambda self: self.device(text="Settings").exists() and self.device(text="Import database").exists()
    )
    @rule()
    def import_an_backup_should_take_effect(self):
        
        self.device(text="Import database").click()
        time.sleep(1)
        self.device(description="Show roots").click()
        time.sleep(1)
        self.device(text="Downloads",resourceId="android:id/title").click()
        time.sleep(1)
        self.device(text="ActivityDiary_Export.sqlite3").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text="A").exists(), "A not exists"

start_time = time.time()

t = Test(
    apk_path="./apk/activitydiary/1.2.5.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/170/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/activitydiary/170.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
