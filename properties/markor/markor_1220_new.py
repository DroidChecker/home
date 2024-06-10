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
        explore_event_count=0,
        diverse_event_count=100,
        main_path_path=None,
        xml_path="None",
        source_activity=None,
        target_activity=None,
        policy_name="pbt",
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            explore_event_count=explore_event_count,
            diverse_event_count=diverse_event_count,
            xml_path=xml_path,
            main_path_path=main_path_path,
            source_activity=source_activity,
            target_activity=target_activity,
            policy_name=policy_name,
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
        
    #bug 1220
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not self.device(text="Settings").exists() and not self.device(text="Date").exists() and not self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def change_file_format_should_work(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
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
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("# test")
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="File settings").click()
        time.sleep(1)
        self.device(text="Format").click()
        time.sleep(1)
        self.device(text="Markdown").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        assert "#" not in self.device(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "1 markdown format failed"
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index].click()
        time.sleep(1)
        assert "#" not in self.device(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "2 markdown format failed"
    


start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1220/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
