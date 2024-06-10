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
        lambda self: self.device(resourceId="com.ichi2.anki:id/flashcard_frame").exists() and
        self.device(resourceId="com.ichi2.anki:id/action_mark_card").exists() and
        self.device(resourceId="com.ichi2.anki:id/bottom_area_layout").exists()
    )
    @rule()
    def reschedule_should_display_another_card(self):
        content = self.device(resourceId="content").child(className="android.view.View").get_text()
        print("content: " + str(content))
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Scheduling").click()
        time.sleep(1)
        self.device(text="Reschedule").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        new_content = self.device(resourceId="content").child(className="android.view.View").get_text()
        print("new_content: " + str(new_content))
        assert content != new_content, "should display another card"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.9alpha55.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5167/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/5167.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
