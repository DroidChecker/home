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
        self.device(description="Add").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)
        self.device(description="Add").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)
        self.device(description="Add").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        time.sleep(1)
        self.device(text="ADD").click()
        time.sleep(1)
    
    @precondition(
        lambda self: self.device(text="Now Playing").exists() and 
        self.device(resourceId="org.y20k.transistor:id/player_textview_station_metadata").exists()
    )
    @rule()
    def exit_app_and_start_again_shouldnot_change_state(self):
        play_text = self.device(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text()
        print("play_text: " + play_text)
        self.device.press("recent")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text() == play_text, "exit app and start again should not change state"

start_time = time.time()


t = Test(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/122/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/transistor/122.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
