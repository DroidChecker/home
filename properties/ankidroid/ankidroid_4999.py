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
        lambda self: self.device(resourceId="com.ichi2.anki:id/deckpicker_name").exists() and 
        self.device(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() 
    )
    @rule()
    def card_browser_should_display_just_selected_deck(self):
        selected_deck = random.choice(self.device(resourceId="com.ichi2.anki:id/deckpicker_name"))
        selected_deck_name = selected_deck.get_text()
        print("selected_deck_name: " + str(selected_deck_name))
        selected_deck.click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(text="Card browser").click()
        time.sleep(1)
        deck_name = self.device(resourceId="com.ichi2.anki:id/dropdown_deck_name").get_text()
        print("deck_name: " + str(deck_name))        
        assert deck_name == selected_deck_name or selected_deck_name in deck_name, "deck name should be the same"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4999/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/4999.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
