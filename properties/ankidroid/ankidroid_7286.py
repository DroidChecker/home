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
        pass

    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/dropdown_deck_name").exists() and
        self.device(resourceId="com.ichi2.anki:id/action_search").exists() and 
        self.device(resourceId="com.ichi2.anki:id/card_sfld").exists()

    )
    @rule()
    def preview_card_should_not_preview_wrong_card(self):
        random_selected_card = random.choice(self.device(resourceId="com.ichi2.anki:id/card_sfld"))
        content = random_selected_card.get_text()
        print("content: " + str(content))
        random_selected_card.long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Preview").click()
        time.sleep(1)
        new_content = self.device(resourceId="qa").get_text()
        print("new_content: " + str(new_content))
        assert content == new_content, "previewed card should be the same as the selected card"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.13.0.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7286/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7286.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
