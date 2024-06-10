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
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)
    
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_hide_unhide_file(self):
        print("time: " + str(time.time() - start_time))
        # first hide a file or folder
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Hide").click()
        time.sleep(1)
        assert not self.device(text=selected_file_name).exists()
        time.sleep(1)
        # unhide a file or folder
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Hidden Files").click()
        time.sleep(1)
        self.device(text=selected_file_name).right(resourceId="com.amaze.filemanager:id/delete_button").click()
        time.sleep(1)
        self.device(text="CLOSE").click()
        time.sleep(1)
        assert self.device(text=selected_file_name).exists(), "unhide file failed with file name: " + str(selected_file_name)

start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1712/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/1712.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
