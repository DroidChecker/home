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
        
        
    #bug 552
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
        self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").exists() and
        self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count > 2 and 
        self.device(text="Markor").exists() and not 
        self.device(text="Settings").exists() and not 
        self.device(text="Date").exists() and not 
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def modify_content_should_update_time(self):
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
        new_content = st.text(alphabet=string.ascii_lowercase,min_size=6, max_size=10).example()
        print("new content: "+str(new_content))
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(new_content)
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        if not self.device(text="Markor").exists():
            self.device.press("back")
        time.sleep(1)
        
        hour_minite = str(self.device(resourceId="com.android.systemui:id/clock").get_text())
        print("hour minite: "+str(hour_minite))
        file_time = self.device(text=file_name).sibling(resourceId="net.gsantner.markor:id/opoc_filesystem_item__description").info['text']
        print("file time: "+str(file_time))
        file_hour_minite = str(file_time.split(" ")[1])
        print("file hour minite: "+str(file_hour_minite))
        assert file_hour_minite == hour_minite

start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/552/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/552_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
