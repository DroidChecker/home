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
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @initialize()
    def set_up(self):
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)
            
    # bug #3560  
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and 
                  self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/search_edit_text").exists() and not
                  self.device(resourceId="com.amaze.filemanager:id/snackBarConstraintLayout").exists()
                  )
    @rule()
    def rule_open_folder(self):
        print("time: " + str(time.time() - start_time))
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file or dir name: "+str(selected_file_name))
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        time.sleep(1)
        if self.device(text="Open with").exists():
            print("its a file, not a folder")
            return
        self.device.press("back")
        time.sleep(1)
        selected_file.click()
        time.sleep(1)
        full_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("full path: "+str(full_path))     
        assert selected_file_name in full_path
        self.device.press("back")
start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/3560/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
