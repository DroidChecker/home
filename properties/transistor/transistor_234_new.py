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
    # 234
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/station_card").exists()
    )
    @rule()
    def cancel_delete_should_not_change_name(self):
        random_selected_station = random.choice(self.device(resourceId="org.y20k.transistor:id/station_card"))
        station_name = random_selected_station.child(resourceId="org.y20k.transistor:id/station_name").get_text()
        print("station_name: " + station_name)
        random_selected_station.fling.horiz.toEnd(max_swipes=1000)
        time.sleep(1)
        self.device(text="Cancel").click()
        time.sleep(1)
        assert self.device(text=station_name).exists(), "NAME changes after cancel delete"

start_time = time.time()

t = Test(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/239/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    run_initial_rules_after_every_mutation=False,
    main_path="main_path/transistor/234_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
