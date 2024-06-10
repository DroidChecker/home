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
        if self.device(text="OK").exists():
            self.device(text="OK").click()

    @precondition(
        lambda self: self.device(resourceId="nl.mpcjanssen.simpletask:id/alertTitle",text="Tag").exists() and 
        self.device(text="OK").exists() and 
        self.device(text="CANCEL").exists() 
    )
    @rule()
    def add_tag(self):   
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        time.sleep(1)
        self.device.set_fastinput_ime(False)
        time.sleep(1)
        self.device(description="Done").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        time.sleep(1)
        assert tag_name in content

start_time = time.time()

t = Test(
    apk_path="./apk/simpletask/10.1.15.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/907/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/simpletask/907.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
