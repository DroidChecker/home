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
        self.device.press("back")

    @precondition(
        lambda self: self.device(text="Episodes").exists() and self.device(text="ALL").exists() and self.device(resourceId="de.danoeh.antennapod:id/status").exists() and not 
        self.device(resourceId="de.danoeh.antennapod:id/txtvInformation").exists()
    )
    @rule()
    def delete_should_update_the_filter_episodes(self):
        self.device(text="ALL").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Filter").click()
        time.sleep(1)
        self.device(text="Downloaded").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        if not self.device(resourceId="de.danoeh.antennapod:id/status").exists():
            print("no episodes found")
            return
        title = self.device(resourceId="de.danoeh.antennapod:id/txtvTitle").get_text()
        print("title: " + title)
        self.device(resourceId="de.danoeh.antennapod:id/txtvTitle").long_click()
        time.sleep(1)
        self.device(text="Delete").click()
        time.sleep(1)
        assert not self.device(text=title).exists(), "episode not deleted"

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/2.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4548/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/4548.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
