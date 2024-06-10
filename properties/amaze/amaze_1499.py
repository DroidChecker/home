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

    @precondition(lambda self: self.device(text="Go Back").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/second").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/fullpath").exists()
                  and self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text() != ".."
                    )
    @rule()
    def rule_go_back(self):
        print("time: " + str(time.time() - start_time))
        original_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("original path: "+str(original_path))
        time.sleep(1)
        self.device(text="Go Back",resourceId="com.amaze.filemanager:id/secondLine").click()
        time.sleep(1)
        after_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("after path: "+str(after_path))
        expected_path = '/'.join(original_path.split("/")[:-1])
        print("expected path: "+str(expected_path))
        assert after_path == expected_path

start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.3.0RC10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1499/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/1499.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
