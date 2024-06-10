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
        
    # 8547
    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/action_search").exists() and 
        self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        self.device(resourceId="com.ichi2.anki:id/dropdown_deck_counts").exists()
    )
    @rule()
    def card_count_should_be_the_same_as_selectall(self):
        card_count = int(self.device(resourceId="com.ichi2.anki:id/dropdown_deck_counts").get_text().split(" ")[0])
        print("card_count: " + str(card_count))
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Select all").click()
        time.sleep(1)
        selected_card_count = int(self.device(resourceId="com.ichi2.anki:id/toolbar_title").get_text())
        print("selected_card_count: " + str(selected_card_count))
        assert card_count == selected_card_count, "card count should be the same as selected card count"



start_time = time.time()


t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/8547/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/8547_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
