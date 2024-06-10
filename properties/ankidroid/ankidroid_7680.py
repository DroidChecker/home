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
        lambda self: self.device(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        self.device(text="Custom study session").exists() and 
        self.device(resourceId="com.ichi2.anki:id/action_sync").exists() and not
        self.device(text="Card browser").exists() 
    )
    @rule()
    def rename_dialog_shouldnot_hide(self):
        self.device(text="Custom study session").long_click()
        time.sleep(1)
        self.device(text="Custom study").click()
        time.sleep(1)
        self.device(text="Review ahead").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)

        assert self.device(text="Rename the existing custom study deck first").exists(), "rename dialog should not hide"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7680/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7680.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
