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

    # 5091
    @precondition(
        lambda self: 
        self.device(textContains="Options for Filtered Deck").exists()
    )
    @rule()
    def option_on_one_filter_deck_should_work(self):
        deck = self.device(textContains="Options for Filtered Deck").get_text()
        deck_name = str(deck.split("for ")[1])
        print("deck_name: " + deck_name)
        self.device(text="Search").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("is:new")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(text="Limit to").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Reschedule")
        time.sleep(1)
        self.device(text="Reschedule").click()
        time.sleep(1)
        self.device(text="Reschedule").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        if self.device(resourceId="com.ichi2.anki:id/action_empty").exists() or self.device(text="STUDY").exists():
            self.device.press("back")
            time.sleep(1)

        assert self.device(text=deck_name).right(resourceId="com.ichi2.anki:id/deckpicker_new").get_text() == "1" or self.device(text=deck_name).right(resourceId="com.ichi2.anki:id/deckpicker_rev").get_text() == "1", "deck_name: " + deck_name + " count: " + self.device(text=deck_name).right(resourceId="com.ichi2.anki:id/deckpicker_new").get_text()

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5091/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/5091_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
