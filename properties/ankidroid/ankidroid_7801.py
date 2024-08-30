import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        d(resourceId="com.ichi2.anki:id/card_checkbox").exists()
    )
    @rule()
    def edit_card_in_preview_shouldnot_switch_to_other(self):
        d(description="More options").click()
        
        d(text="Preview").click()
        
        content = d(resourceId="qa").get_text()
        print("content: " + str(content))
        
        d(resourceId="com.ichi2.anki:id/action_edit").click()
        
        d(resourceId="com.ichi2.anki:id/note_deck_spinner").click()
        
        random.choice(d(resourceId="android:id/text1")).click()
        
        d(resourceId="com.ichi2.anki:id/action_save").click()
        
        assert d(resourceId="qa").exists()
        new_content = d(resourceId="qa").get_text()
        print("new_content: " + str(new_content))
        assert content == new_content, "content should not change"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.13.0.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7801/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7801.json"
)
run_android_check_as_test(t,setting)

