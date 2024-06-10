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
        lambda self: 
        self.device(resourceId="com.ichi2.anki:id/fab_main").exists() and
        self.device(description="More options").exists() and not 
        self.device(text="Card browser").exists()
    )
    @rule()
    def right_swipe_from_the_center_should_not_open_the_menu(self):
        print("precondition satisfied, executing.")
        # right swipe
        self.device.drag(0.5, 0.5, 0.9, 0.5)
        time.sleep(1)
        assert not self.device(resourceId="com.ichi2.anki:id/design_menu_item_text").exists(), "mistakenly open the menu"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.15.0.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/8235/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/8235.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
