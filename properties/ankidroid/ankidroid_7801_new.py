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
        lambda self: 
        self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        self.device(resourceId="com.ichi2.anki:id/card_checkbox").exists()
    )
    @rule()
    def edit_card_in_preview_shouldnot_switch_to_other(self):
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Preview").click()
        time.sleep(1)
        content = self.device(resourceId="qa").get_text()
        print("content: " + str(content))
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_edit").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/note_deck_spinner").click()
        time.sleep(1)
        random.choice(self.device(resourceId="android:id/text1")).click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_save").click()
        time.sleep(1)
        assert self.device(resourceId="qa").exists()
        new_content = self.device(resourceId="qa").get_text()
        print("new_content: " + str(new_content))
        assert content == new_content, "content should not change"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7801/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7801.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
