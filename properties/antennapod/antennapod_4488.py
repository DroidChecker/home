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
        if not self.device(text="Setting").exists() and self.device(description="Open menu").exists():
            self.device(description="Open menu").click()
            time.sleep(1)

    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").exists() and
          self.device(resourceId="de.danoeh.antennapod.debug:id/search_src_text").exists() and 
          self.device(resourceId="de.danoeh.antennapod.debug:id/coverHolder").exists()
    )
    @rule()
    def search_in_one_podcast_should_not_display_others(self):
        assert int(self.device(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").count) == 1, "discovery cover count not 1"

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/2.0.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4488/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/4488.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
