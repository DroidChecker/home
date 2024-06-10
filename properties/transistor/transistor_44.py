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

    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/list_item_more_button").exists() and self.device(resourceId="org.y20k.transistor:id/list_item_playback_indicator").exists()
    )
    @rule()
    def rename_station_not_change_station_state(self):
        playing_station_name = self.device(resourceId="org.y20k.transistor:id/list_item_playback_indicator").sibling(resourceId="org.y20k.transistor:id/list_item_textview").get_text()
        print("playing_station_name: " + playing_station_name)
        self.device(resourceId="org.y20k.transistor:id/list_item_playback_indicator").sibling(resourceId="org.y20k.transistor:id/list_item_more_button").click()
        time.sleep(1)
        self.device(text="Rename").click()
        time.sleep(1)
        original_name = self.device(resourceId="org.y20k.transistor:id/dialog_rename_station_input").get_text()
        print("original_name: " + original_name)
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("new_name: " + new_name)
        self.device(resourceId="org.y20k.transistor:id/dialog_rename_station_input").set_text(new_name)
        time.sleep(1)
        self.device(text="RENAME").click()
        time.sleep(1)
        assert self.device(text=new_name).exists(), "NEW NAME DOES NOT EXIST"
        assert not self.device(text=original_name).exists(), "OLD NAME STILL EXISTS"
        assert self.device(resourceId="org.y20k.transistor:id/list_item_playback_indicator").sibling(resourceId="org.y20k.transistor:id/list_item_textview").get_text() == new_name, "station state changed"

start_time = time.time()

t = Test(
    apk_path="./apk/transistor/1.2.1.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/44/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/transistor/44.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
