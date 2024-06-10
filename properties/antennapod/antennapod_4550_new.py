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
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/toolbar").exists() and 
        self.device(resourceId="de.danoeh.antennapod:id/toolbar").child(text="Episodes",className="android.widget.TextView").exists() and 
        self.device(resourceId="de.danoeh.antennapod:id/action_favorites").exists() and not 
        self.device(resourceId="de.danoeh.antennapod:id/container").exists() and not 
        self.device(text="Settings").exists()
    )
    @rule()
    def text_should_display_when_episodes_is_empty(self):

        assert self.device(resourceId="de.danoeh.antennapod:id/emptyViewTitle").exists(), "empty view title not found"

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4550/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
