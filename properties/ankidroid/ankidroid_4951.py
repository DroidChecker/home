import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

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
        grant_perm = True,
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
            grant_perm = grant_perm,
            main_path=main_path
        )   

    @precondition(
        lambda self: d(text="AnkiDroid").exists() and
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        d(resourceId="com.ichi2.anki:id/deckpicker_name").exists()
    )
    @rule()
    def rule_allow_permission_three_points_exists(self):
        
        assert d(description="More options").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9alpha29.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4951/mutate/1",
    policy_name="random",

    grant_perm=False,
    main_path="main_path/ankidroid/4951.json"
)
run_android_check_as_test(t,setting)

