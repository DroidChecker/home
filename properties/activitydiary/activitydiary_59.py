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
        lambda self: self.device(text="Manage Activities").exists() and self.device(resourceId="de.rampro.activitydiary.debug:id/action_add_activity").exists() and self.device(description="Navigate up").exists() and self.device(resourceId="de.rampro.activitydiary.debug:id/activity_name").exists()
    )
    @rule()
    def delete_activity(self):
        activity_count = int(self.device(resourceId="de.rampro.activitydiary.debug:id/activity_name").count)
        print("activity count: " + str(activity_count))
        selected_activity_index = random.randint(0, activity_count - 1)
        selected_activity = self.device(resourceId="de.rampro.activitydiary.debug:id/activity_name")[selected_activity_index]
        selected_activity_name = selected_activity.get_text()
        print("selected activity: " + selected_activity_name)
        selected_activity.click()
        time.sleep(1)
        self.device(resourceId="de.rampro.activitydiary.debug:id/action_edit_delete").click()
        time.sleep(1)
        assert self.device(text=selected_activity_name).exists() == False, "activity not deleted"

start_time = time.time()

t = Test(
    apk_path="./apk/activitydiary/1.0.0.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/59/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/activitydiary/59.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
