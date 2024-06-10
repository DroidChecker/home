import string
from main import *
import time
import sys
import re

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
    
    # bug #389
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
                  self.device(resourceId="net.gsantner.markor:id/note_title").count < 4)
    @rule()
    def create_file_should_only_create_one(self):
        file_count = int(self.device(resourceId="net.gsantner.markor:id/note_title").count)
        print("file_count: " + str(file_count))
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        content = st.text(alphabet=string.ascii_lowercase,min_size=5, max_size=6).example()
        print("content: " + str(content))
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(content)
        time.sleep(1)
        self.device.press("back")
        if self.device(resourceId="net.gsantner.markor:id/action_preview").exists():
            self.device.press("back")
        time.sleep(1)
        new_count = int(self.device(resourceId="net.gsantner.markor:id/note_title").count)
        print("new_count: " + str(new_count))
        assert new_count == file_count + 1
        
start_time = time.time()

t = Test(
    apk_path="./apk/markor/1.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/389/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/389.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
