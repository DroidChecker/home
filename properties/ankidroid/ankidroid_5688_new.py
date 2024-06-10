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
        self.device(text="Get Started").click()

    @precondition(
        lambda self: self.device(text="Preview").exists() and
        self.device(resourceId="com.ichi2.anki:id/preview_next_flashcard").exists() and 
        self.device(resourceId="qa").exists() and 
        self.device(resourceId="qa").get_text() != ""
    )
    @rule()
    def rotate_device_should_keep_review_card(self):
        card_content = self.device(resourceId="qa").get_text()
        print("card_content: " + str(card_content))
        self.device.set_orientation("l")
        time.sleep(1)
        self.device.set_orientation("n")
        time.sleep(1)
        new_card_content = self.device(resourceId="qa").get_text()
        print("new_card_content: " + str(new_card_content))
        assert card_content == new_card_content, "card content should not change"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5688/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 10
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
