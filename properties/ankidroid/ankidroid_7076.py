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
        lambda self: self.device(text="考研").exists() and self.device(text="例句").exists() and 
        self.device(resourceId="com.ichi2.anki:id/action_sync").exists()
    )
    @rule()
    def should_display_name_of_sub_deck(self):
        self.device(text="考研").click()
        time.sleep(1)
        assert self.device(text="例句").exists(), "例句 not found"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.14alpha1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7076/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/7076.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
