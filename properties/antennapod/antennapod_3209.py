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

    @precondition(
        lambda self: self.device(text="FAVORITES").exists() and self.device(text="FAVORITES").info['selected'] and self.device(resourceId="de.danoeh.antennapod:id/txtvTitle").exists() and not self.device(resourceId="de.danoeh.antennapod:id/nav_list").exists()
    )
    @rule()
    def remove_favorite(self):

        selected_title = random.choice(self.device(resourceId="de.danoeh.antennapod:id/container"))
        selected_title_name = selected_title.child(resourceId="de.danoeh.antennapod:id/txtvTitle").info['text']
        print("title: " + selected_title_name)
        selected_title.long_click()
        time.sleep(1)
        self.device(text="Remove from Favorites").click()
        time.sleep(1)
        assert not (self.device(resourceId="de.danoeh.antennapod:id/container").exists() and 
                    self.device(resourceId="de.danoeh.antennapod:id/container").child(resourceId="de.danoeh.antennapod:id/txtvTitle", text=selected_title_name).exists())
start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/1.7.2b.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/3209/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/3209.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
