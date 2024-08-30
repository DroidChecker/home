import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/action_search").exists() and 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        d(resourceId="com.ichi2.anki:id/dropdown_deck_counts").exists()
    )
    @rule()
    def card_count_should_be_the_same_as_selectall(self):
        card_count = int(d(resourceId="com.ichi2.anki:id/dropdown_deck_counts").get_text().split(" ")[0])
        print("card_count: " + str(card_count))
        d(description="More options").click()
        
        d(text="Select all").click()
        
        selected_card_count = int(d(resourceId="com.ichi2.anki:id/toolbar_title").get_text())
        print("selected_card_count: " + str(selected_card_count))
        assert card_count == selected_card_count, "card count should be the same as selected card count"
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.15alpha38.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/8547/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/8547.json"
)
run_android_check_as_test(t,setting)

