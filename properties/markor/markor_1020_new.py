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
        time.sleep(1)
    
    
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").exists() 
        )
    @rule()
    def file_type_should_be_the_same(self):
        file_type = self.device(resourceId="net.gsantner.markor:id/new_file_dialog__type").child(className="android.widget.TextView").get_text()
        print("file_type: " + file_type)
        file_name_suffix = self.device(resourceId="net.gsantner.markor:id/new_file_dialog__ext").get_text()
        print("file_name_suffix: " + file_name_suffix)
        if file_type == "Markdown":
            assert file_name_suffix == ".md"
        elif file_type == "Plain Text":
            assert file_name_suffix == ".txt"
        elif file_type == "todo.txt":
            assert file_name_suffix == ".todo.txt"
        elif file_type == "AsciiDoc":
            assert file_name_suffix == ".adoc"
        elif file_type == "CSV":
            assert file_name_suffix == ".csv"
        elif file_type == "OrgMode":
            assert file_name_suffix == ".org"
        elif file_type == "Wikitext":
            assert file_name_suffix == ".txt"
        else:
            assert file_name_suffix == ".md"
        

start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1020/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/1020_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
