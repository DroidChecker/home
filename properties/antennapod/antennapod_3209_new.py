from main import *
import time
import sys


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
        pass

    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/toolbar").exists() and 
        self.device(resourceId="de.danoeh.antennapod:id/toolbar").child(text="Episodes",className="android.widget.TextView").exists() and
        self.device(resourceId="de.danoeh.antennapod:id/txtvTitle").exists() and not 
        self.device(resourceId="de.danoeh.antennapod:id/navDrawerFragment").exists() and not 
        self.device(text="Filtered").exists()
    )
    @rule()
    def remove_or_add_favorite(self):
        selected_title = random.choice(self.device(resourceId="de.danoeh.antennapod:id/txtvTitle"))
        selected_title_name = selected_title.info['text']
        print("title: " + selected_title_name)
        selected_title.long_click()
        time.sleep(1)
        remove_or_add = True
        if self.device(text="Remove from favorites").exists():
            print("remove")
            self.device(text="Remove from favorites").click()
        else:
            print("add")
            self.device(text="Add to favorites").click()
            remove_or_add = False
        time.sleep(1)
        if remove_or_add:
            assert not self.device(text=selected_title_name).exists() or not self.device(text=selected_title_name).sibling(resourceId="de.danoeh.antennapod:id/status").child(resourceId="de.danoeh.antennapod:id/isFavorite").exists(), "remove failed"
        else:
            assert self.device(text=selected_title_name).sibling(resourceId="de.danoeh.antennapod:id/status").child(resourceId="de.danoeh.antennapod:id/isFavorite").exists(), "add failed"


start_time = time.time()


t = Test(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/3209/mutate_new/1",
    policy_name="mutate",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/3209_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
