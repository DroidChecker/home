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
        self.device(description="Open menu").click()
        time.sleep(1)
        self.device(text="Add podcast").click()
        time.sleep(1)
        if self.device(text="Show suggestions").exists():
            self.device(text="Show suggestions").click()
            time.sleep(1)
        random.choice(self.device(resourceId="de.danoeh.antennapod:id/discovery_cover")).click()
        time.sleep(3)
        self.device(text="Subscribe").click()
        
    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/container").exists() and
          self.device(resourceId="de.danoeh.antennapod:id/search_src_text").exists() and 
          self.device(resourceId="de.danoeh.antennapod:id/feed_title_chip").exists()
    )
    @rule()
    def search_in_one_podcast_should_not_display_others(self):
        podcast_name = self.device(resourceId="de.danoeh.antennapod:id/feed_title_chip").get_text()
        print("podcast name: " + podcast_name)
        random.choice(self.device(resourceId="de.danoeh.antennapod:id/container")).click()
        name = self.device(resourceId="de.danoeh.antennapod:id/txtvPodcast").get_text()
        print("name: " + name)
        assert name == podcast_name, "name not equal to podcast name"

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4488/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/4488_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
