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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        
    
    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_rename_file(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        is_file = True
        if "." not in file_name:
            is_file = False
            print("not a file")
            return
        file_name_suffix = file_name.split(".")[-1]
        print("file name: "+str(file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        if is_file:
            name = name+"."+file_name_suffix
        print("new file name: "+str(name))
        self.device(resourceId="net.gsantner.markor:id/new_name").set_text(name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        assert self.device(text=name).exists()


start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1961/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
