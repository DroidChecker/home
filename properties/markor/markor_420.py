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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        
    @precondition(lambda self: self.device(text="Select entries").exists() and 
                  self.device(resourceId="net.gsantner.markor:id/note_title").exists()
                  )
    @rule()
    def selection_should_discard_after_clicking_new(self):
        selected_info = self.device(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
        number_of_selected = selected_info.split(" ")[0]
        if number_of_selected == "One":
            number_of_selected = 1
        number_of_selected = int(number_of_selected)
        random.choice(self.device(resourceId="net.gsantner.markor:id/note_title")).click()
        time.sleep(1)
        if self.device(text="Select entries").exists():
            new_selected_info = self.device(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
            new_number_of_selected = new_selected_info.split(" ")[0]
            if new_number_of_selected == "One":
                new_number_of_selected = 1
            new_number_of_selected = int(new_number_of_selected)
            assert new_number_of_selected == number_of_selected - 1 or new_number_of_selected == number_of_selected + 1, "number of selected not correct"

        
start_time = time.time()

t = Test(
    apk_path="./apk/markor/1.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/420/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/markor/420.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
