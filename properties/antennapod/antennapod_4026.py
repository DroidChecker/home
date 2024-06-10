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
        lambda self: self.device(text="Queue").exists() and 
        self.device(resourceId="de.danoeh.antennapod.debug:id/queue_lock").exists() and
        self.device(resourceId="de.danoeh.antennapod.debug:id/txtvTitle").exists() and
        self.device(resourceId="de.danoeh.antennapod.debug:id/audioplayerFragment").exists() and not
        self.device(text="Settings").exists()
    )
    @rule()
    def play_episode_should_add_to_queue(self):
        title = self.device(resourceId="de.danoeh.antennapod.debug:id/audioplayerFragment").child(resourceId="de.danoeh.antennapod.debug:id/txtvTitle").get_text()
        print("title: " + title)
        assert not self.device(resourceId="de.danoeh.antennapod.debug:id/emptyViewTitle").exists(), "Queue is empty"
        assert self.device(resourceId="de.danoeh.antennapod.debug:id/recyclerView").child(text=title).exists() and self.device(scrollable=True,resourceId="de.danoeh.antennapod.debug:id/recyclerView").scroll.to(text=title), "Episode is not in queue"

        

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/2.0.0-alpha1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4026/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/4026.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
