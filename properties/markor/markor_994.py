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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        time.sleep(1)
        
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").exists() and
        self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count >= 2 and 
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not 
        self.device(text="Settings").exists() and not 
        self.device(text="Date").exists() and not 
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def create_file_with_same_name_should_not_overwrite(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/ui__filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        file_name_suffix = file_name.split(".")[-1]
        file_name_prefix = file_name.split(".")[0]
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        time.sleep(1)
        original_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original content: "+str(original_content))
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(file_name_prefix)
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__ext").set_text("."+file_name_suffix)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        new_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("new content: "+str(new_content))
        assert original_content == new_content, "create file with same name should not overwrite"
start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.2.10.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/994/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/994.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
