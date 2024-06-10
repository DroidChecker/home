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
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="AnkiDroid").click()
        time.sleep(1)
        self.device(text="Language").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="日本語")
        time.sleep(1)
        self.device(text="日本語").click()
        time.sleep(1)

    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        self.device(resourceId="com.ichi2.anki:id/action_search").exists() 
    )
    @rule()
    def card_info_should_be_translated(self):
        self.device(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/toolbar").child(className="android.widget.ImageView").click()
        time.sleep(1)
        assert not self.device(text="Card Info").exists(), "Card Info found"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7758/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7758.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
