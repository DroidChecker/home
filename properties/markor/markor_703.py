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
        lambda self: self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and 
         self.device(resourceId="net.gsantner.markor:id/action_preview").exists() and not
         self.device(text="Settings").exists() and not 
         self.device(text="Date").exists() and not 
         self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def format_change_should_work_in_view_mode(self):
        
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("# test")
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Format").click()
        time.sleep(1)
        self.device(text="Markdown").click()
        time.sleep(1)
        assert not "#" in str(self.device(className="android.webkit.WebView").child(className="android.view.View").info["text"])


start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.1.3.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/703/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/703.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
