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

    @precondition(lambda self: self.device(textContains="Search results of").exists() and not 
                  self.device(resourceId="com.amaze.filemanager:id/telegram").exists() and 
                  self.device(resourceId="com.amaze.filemanager:id/firstline").exists()
    )
    @rule()
    def rule_search(self):
        search_text = self.device(textContains="Search results of").get_text()
        print("search_text: " + search_text)
        search_word = search_text.split(" ")[-1]
        print("search_word: " + search_word)
        file_name = self.device(resourceId="com.amaze.filemanager:id/firstline")
        for i in range(file_name.count):
            assert search_word.lower() in file_name[i].get_text().lower(), "search_word: " + search_word + " file_name: " + file_name[i].get_text()


start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.5.0.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1797/random_100/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/amaze/1797.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
