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
        lambda self: self.device(resourceId="net.gsantner.markor:id/action_edit").exists() and
          self.device(className="android.webkit.WebView").child(className="android.view.View").exists() and not
          self.device(text="todo").exists()
        )
    @rule()
    def format_should_retain_next_time_open_it(self):
        content = self.device(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content: "+str(content))
        title = self.device(resourceId="net.gsantner.markor:id/note__activity__text_note_title").get_text()
        print("title: "+str(title))
        self.device.press("back")
        time.sleep(1)
        if self.device(resourceId="net.gsantner.markor:id/action_edit").exists():
            self.device.press("back")
            time.sleep(1)
        self.device(textStartsWith=title).click()
        time.sleep(1)
        if self.device(resourceId="net.gsantner.markor:id/action_preview").exists():
            self.device(resourceId="net.gsantner.markor:id/action_preview").click()
            time.sleep(1)
        content2 = self.device(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content2: "+str(content2))
        assert content == content2
start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.5.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1220/random_100/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/1220.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
