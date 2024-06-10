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
        self.device(text="Add a new station").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)

        self.device(text="Add a new station").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)

        self.device(text="Add a new station").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/player_playback_button").exists()
    )
    @rule()
    def station_name_should_be_consistent(self):
        station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        self.device(resourceId="org.y20k.transistor:id/player_playback_button").click()
        time.sleep(1)
        assert self.device(resourceId="org.y20k.transistor:id/player_station_name",text=station_name).exists(), "NAME changes after playback"

start_time = time.time()

t = Test(
    apk_path="./apk/transistor/3.0.2.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/164/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/transistor/164.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
