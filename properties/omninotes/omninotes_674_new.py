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
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/done").click()
        time.sleep(1)
        if self.device(text="OK").exists():
            self.device(text="OK").click()
            time.sleep(1)
    
    
    @precondition(lambda self: self.device(text="Interface").exists() and self.device(text="Language").exists())
    @rule()
    def check_languge_selection(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Language").click()
        time.sleep(1)
        assert self.device(scrollable=True).scroll.to(text="Suomi (Finnish)"), "Finnish"
        
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/674/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/674.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
