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
        
    # 1478 在最新版本上有bug
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
        self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").exists() and 
        int(self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count) > 2 and 
        self.device(resourceId="net.gsantner.markor:id/nav_notebook").info["selected"] and 
        self.device(resourceId="net.gsantner.markor:id/action_go_to").exists()
    )
    @rule()
    def view_file_should_exist_in_recent_viewed_documents(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        if not self.device(resourceId="net.gsantner.markor:id/action_go_to").exists():
            self.device.press("back")
            time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_go_to").click()
        time.sleep(1)
        self.device(text="Recently viewed documents").click()
        time.sleep(1)
        assert self.device(text=file_name).exists(), "file not in recently viewed documents"


start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1478/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/1478_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
