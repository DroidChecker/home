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
        lambda self: self.device(text="Download").exists() and self.device(text="Stream").exists() and self.device(resourceId="de.danoeh.antennapod:id/visit_website_item").exists()
    )
    @rule()
    def change_setting_should_not_influence_Download_function(self):
        self.device(text="Download").click()
        time.sleep(1)
        assert self.device(text="Delete").exists() or self.device(text="Cancel").exists()

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/1.8.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/3786/random_100/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/3786.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
