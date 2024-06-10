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

    @precondition(lambda self: self.device(textContains=".zip").exists() and not self.device(text="Internal Storage").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(text="Cloud Connection").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def extract_zip_file_shouldnot_need_password(self):
        print("time: " + str(time.time() - start_time))
        zip_file = self.device(textContains=".zip")
        folder_name = zip_file.get_text().split(".")[0]
        print("zip_file: "+str(zip_file.get_text()))
        zip_file.click()
        time.sleep(1)
        self.device(text="EXTRACT").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/listView").child_by_text(folder_name,allow_scroll_search=True,resourceId="com.amaze.filemanager:id/firstline").exists(), "extract zip file failed with zip file name: "+str(zip_file.get_text())

start_time = time.time()

t = Test(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1834/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
