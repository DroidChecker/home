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
        lambda self: self.device(resourceId="de.danoeh.antennapod.debug:id/add_to_favorites_item").exists() and 
        self.device(description="Audio controls") and 
        self.device(resourceId="de.danoeh.antennapod.debug:id/sbPosition").exists()
    )
    @rule()
    def remove_podcast_should_close_miniplayed(self):
        title = self.device(resourceId="de.danoeh.antennapod.debug:id/txtvEpisodeTitle").get_text()
        print("title: " + title)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Open Podcast").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Remove podcast").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(3)
        assert not self.device(resourceId="de.danoeh.antennapod.debug:id/txtvAuthor").exists() and not self.device(resourceId="de.danoeh.antennapod.debug:id/butPlay").exists(), "miniplayer not closed"
        
start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/2.2.0-beta1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/5003/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/5003.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
