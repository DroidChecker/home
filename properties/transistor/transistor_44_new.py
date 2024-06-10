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
        main_path=None,
        run_initial_rules_after_every_mutation=True
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
            main_path=main_path,
            run_initial_rules_after_every_mutation=run_initial_rules_after_every_mutation
        )

    @initialize()
    def set_up(self):
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Edit Stations")
        time.sleep(1)
        self.device(text="Edit Stations").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        for _ in range(3):
            self.device(text="Add new station").click()
            time.sleep(1)
            station_name_prefix = ["bbc", "new", "swi","chn"]
            selected_station_name_prefix = random.choice(station_name_prefix)
            self.device(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
            time.sleep(3)
            random_selected_station = random.choice(self.device(resourceId="org.y20k.transistor:id/station_name"))
            random_selected_station.click()
            time.sleep(1)
            self.device(text="Add").click()
            time.sleep(1)

    # 44
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/player_station_name").exists() and 
        self.device(resourceId="org.y20k.transistor:id/station_name", text=self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()).exists() and not
        self.device(text="Save Changes").exists()
    )
    @rule()
    def rename_station_not_change_station_state(self):
        playing_station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("playing_station_name: " + playing_station_name)
        self.device(resourceId="org.y20k.transistor:id/station_name", text=playing_station_name).long_click()
        time.sleep(1)
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=5).example()
        print("new_name: " + new_name)
        self.device(resourceId="org.y20k.transistor:id/edit_station_name").set_text(new_name)
        time.sleep(2)
        self.device(text="Save Changes").click()
        time.sleep(1)
        assert self.device(resourceId="org.y20k.transistor:id/station_name", text=new_name).exists(), "NEW NAME DOES NOT EXIST in station"
        assert self.device(resourceId="org.y20k.transistor:id/player_station_name", text=new_name).exists(), "NEW NAME DOES NOT EXIST in player"
        assert not self.device(resourceId="org.y20k.transistor:id/station_name", text=playing_station_name).exists(), "OLD NAME STILL EXISTS"
        
start_time = time.time()

t = Test(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/44/mutate_new/1",
    policy_name="mutate",
    timeout=43200,
    number_of_events_that_restart_app = 100,
    run_initial_rules_after_every_mutation=False,
    main_path="main_path/transistor/44_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
