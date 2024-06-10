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
        
        
    
    # bug #1961
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and 
                  self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text() is not None and 
                  self.device(resourceId="net.gsantner.markor:id/action_search").exists())
    @rule()
    def search_in_the_file(self):
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        time.sleep(1)
        words = content.split()
        search_word = random.choice(words)
        print("search word: "+str(search_word))
        self.device(resourceId="net.gsantner.markor:id/action_search").click()
        time.sleep(1)
        self.device(text="Search").set_text(search_word)
        time.sleep(1)
        search_result = self.device(resourceId="android:id/text1")
        search_result_count = search_result.count
        print("search result count: "+str(search_result_count))
        assert search_result_count > 0
        search_result_text = search_result.info['text']
        print("search result text: "+str(search_result_text))
        assert search_word in str(search_result_text)


start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1961/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/1961_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
