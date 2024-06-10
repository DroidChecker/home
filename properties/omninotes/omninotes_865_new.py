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
        
        
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def sroll_down_on_attachment(self):
        print("time: " + str(time.time() - start_time))
        self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").click()
        time.sleep(1)
        if self.device(text="Pushbullet").exists():
            return True
        if self.device(scrollable=True).exists():
            self.device(scrollable=True).scroll(steps=10)
        time.sleep(1)
        assert self.device(text="Pushbullet").exists()
    
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.1.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/865/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/865.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
