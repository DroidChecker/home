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
        lambda self: self.device(text="Activity Diary").exists() and not self.device(text="<No Activity>").exists() and self.device(description="Statistics").info["selected"] and not self.device(text="Settings").exists()
    )
    @rule()
    def click_content_should_enter_diary_entry(self):
        activity_name = self.device(resourceId="de.rampro.activitydiary:id/activity_name").get_text() 
        self.device(resourceId="de.rampro.activitydiary:id/duration_label").click()
        time.sleep(1)
        assert self.device(text="Diary entry").exists(), "not enter diary entry"
        time.sleep(1)
        current_activity_name = self.device(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        assert current_activity_name == activity_name, "activity name changed from "+ activity_name + " to " + current_activity_name
start_time = time.time()

t = Test(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/253/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
