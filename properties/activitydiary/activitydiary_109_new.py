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
        lambda self: self.device(text="New activity").exists() and self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").exists()
    )
    @rule()
    def new_activity_name(self):
        name = st.text(alphabet=string.digits + string.ascii_letters + string.punctuation,min_size=1, max_size=5).example()
        print(name)
        self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").set_text(name)
        time.sleep(1)
        if self.device(resourceId="de.rampro.activitydiary:id/textinput_error").exists():
            self.device(description="Navigate up").click()
            time.sleep(1)
            assert self.device(resourceId="de.rampro.activitydiary:id/activity_name",text=name).exists() , "activity name not exists"

start_time = time.time()

t = Test(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/109/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
