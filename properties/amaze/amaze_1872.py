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
            
    @precondition(lambda self: 
                  self.device(resourceId="com.amaze.filemanager:id/search").exists() and not 
                  self.device(text="Internal Storage").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/cpy").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/firstline").exists()
    )
    @rule()
    def search_folder_should_be_opened(self):
        print("time: " + str(time.time() - start_time))
        folder_count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("folder count: "+str(folder_count))
        folder = None
        for i in range(folder_count):
            folder_index = random.randint(0, folder_count-1)
            print("folder index: "+str(folder_index))
            folder_ui = self.device(resourceId="com.amaze.filemanager:id/firstline")[folder_index]
            folder_ui_name = folder_ui.get_text()          
            if "." in folder_ui_name:
                continue
            folder = folder_ui
            folder_name = folder_ui_name
            break
        if folder is None:
            print("no folder found")
            return
        print("folder name: "+str(folder_name))
        folder.click()
        time.sleep(1)
        assert not self.device(text="Open As").exists(), "open folder failed with folder name: "+str(folder_name)


start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1872/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/1872.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
