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
        self.device(resourceId="com.ichi2.anki:id/dropdown_deck_name").exists() 
    )
    @rule()
    def reposition_should_not_be_missing(self):
        random_select_card = random.choice(self.device(resourceId="com.ichi2.anki:id/card_sfld"))
        random_select_card.long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Reposition").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/dialog_text_input").set_text("1")
        time.sleep(1)
        self.device(resourceId="android:id/button1").click()
        time.sleep(1)
        # go to "more" and check
        self.device(description="More options").click()
        time.sleep(1)
        assert self.device(text="Undo reposition").exists(), "missing Undo reposition"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7674/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7674_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
