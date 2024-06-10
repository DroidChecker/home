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

    @precondition(
        lambda self: 
        self.device(resourceId="com.ichi2.anki:id/new_number").exists() and
        self.device(resourceId="com.ichi2.anki:id/answer_field").exists() and 
        self.device(resourceId="com.ichi2.anki:id/answer_field").get_text() != "Type answer" and
        self.device(resourceId="com.ichi2.anki:id/answer_options_layout").exists()
    )
    @rule()
    def text_should_display_after_type_answer(self):
        typed_text = self.device(resourceId="com.ichi2.anki:id/answer_field").get_text()
        print("typed_text: " + typed_text)
        self.device(resourceId="com.ichi2.anki:id/answer_options_layout").click()
        time.sleep(1)
        for view in self.device(resourceId="content").child(className="android.view.View"):
            print("view text: " + view.get_text())
            if typed_text in view.get_text():
                return True 
        assert False, "text should display after type answer"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5334/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
