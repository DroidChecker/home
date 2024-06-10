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
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/butPlay").exists() and 
        self.device(description="More options").exists() and 
        self.device(resourceId="de.danoeh.antennapod:id/add_to_favorites_item").exists()
    )
    @rule()
    def click_podcast_should_work(self):
        self.device(description="More options").click() 
        time.sleep(1)
        self.device(text="Open podcast").click()
        time.sleep(1)
        assert not self.device(resourceId="de.danoeh.antennapod:id/butFF").exists()



start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4010/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
