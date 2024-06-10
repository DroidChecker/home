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
        lambda self: self.device(text="Activity Diary").exists() and self.device(resourceId="de.rampro.activitydiary:id/select_card_view").exists() and not self.device(text="Settings").exists()
    )
    @rule()
    def long_click_activity_should_edit_it(self):
        # random select an activity
        activity_count = self.device(resourceId="de.rampro.activitydiary:id/select_card_view").count
        random_index = random.randint(0, activity_count - 1)
        selected_activity = self.device(resourceId="de.rampro.activitydiary:id/select_card_view")[random_index]
        activity_name = selected_activity.child(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("activity name: " + activity_name)
        time.sleep(1)
        selected_activity.long_click()
        time.sleep(1)
        current_activity_name = self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").get_text()
        assert current_activity_name == activity_name, "activity name not match "+ str(activity_name) + " " + str(current_activity_name)
start_time = time.time()


t = Test(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/176/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
