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

    # 1797
    @precondition(lambda self: self.device(text="Type to search…").exists())
    @rule()
    def rule_search(self):
        print("time: " + str(time.time() - start_time))
        characters = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=1).example()
        print("characters: "+str(characters))
        self.device(text="Type to search…").set_text(characters)
        time.sleep(1)
        self.device.set_fastinput_ime(False)
        time.sleep(1)
        self.device.send_action("search")
        time.sleep(1)
        self.device.set_fastinput_ime(True)
        file_name = self.device(resourceId="com.amaze.filemanager:id/searchItemFileNameTV")
        if file_name.count == 0:
            print("no file found")
            return
        for i in range(file_name.count):
            assert characters in file_name[i].get_text().lower(), "characters: " + characters + " file_name: " + file_name[i].get_text().lower()

start_time = time.time()


t = Test(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1797/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
