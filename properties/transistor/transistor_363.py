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
        self.device(text="ADD NEW STATION").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        time.sleep(1)
        self.device(text="ADD").click()

        self.device(text="ADD NEW STATION").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        time.sleep(1)
        self.device(text="ADD").click()

        self.device(text="ADD NEW STATION").click()
        time.sleep(1)
        self.device(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        time.sleep(1)
        self.device(text="ADD").click()

    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/station_card").exists() and self.device(resourceId="org.y20k.transistor:id/station_card").count > 1 and self.device(resourceId="org.y20k.transistor:id/player_play_button").exists()
    )
    @rule()
    def notification_button_should_work(self):
        station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        self.device(resourceId="org.y20k.transistor:id/player_play_button").click()
        time.sleep(1)
        self.device.open_notification()
        time.sleep(1)
        if not self.device(description="Next").exists():
            self.device.press("back")
            return
        self.device(description="Next").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        new_station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("new_station_name: " + new_station_name)
        assert station_name != new_station_name, "notification next button does not work"

start_time = time.time()

t = Test(
    apk_path="./apk/transistor/4.0.15.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/363/mutate/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/transistor/363.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
