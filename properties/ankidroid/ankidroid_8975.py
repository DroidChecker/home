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
        lambda self: self.device(resourceId="com.ichi2.anki:id/action_search").exists() and 
        self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() 
    )
    @rule()
    def card_should_be_searched_in_all_decks(self):
        text = self.device(resourceId="com.ichi2.anki:id/card_sfld").get_text()
        print("text: " + str(text))
        # random select a substring of the text
        selected_text = random.choice(text.split(" "))
        print("selected_text: " + str(selected_text))
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/dropdown_deck_name").click()
        time.sleep(1)
        self.device(text="Default").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_search").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/search_src_text").set_text(selected_text)
        time.sleep(1)
        self.device.set_fastinput_ime(False) # 
        self.device.send_action("search") # 
        time.sleep(1)
        self.device(text="SEARCH ALL DECKS").click()
        time.sleep(1)
        assert self.device(resourceId="com.ichi2.anki:id/card_sfld").exists(), "card not found"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.15.2.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/8975/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/8975.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
