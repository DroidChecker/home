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
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @precondition(
        lambda self: self.device(text="Add new station").exists() and 
        self.device(className="android.widget.EditText").get_text() != "Paste a valid streaming URL"     
    )
    @rule()
    def should_add_station(self):
        print(self.device(className="android.widget.EditText").get_text())
        self.device(text="ADD").click()
        time.sleep(3)
        if self.device(text="Download Issue").exists():
            print("Download Issue")
            return
        assert self.device(resourceId="org.y20k.transistor:id/list_item_textview").exists() 

start_time = time.time()

t = Test(
    apk_path="./apk/transistor/1.1.4.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/9/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
