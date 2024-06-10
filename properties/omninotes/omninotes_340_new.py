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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
            time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/done").click()
        time.sleep(1)
        if self.device(text="OK").exists():
            self.device(text="OK").click()
            time.sleep(1) 

    # bug #340
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/count").exists() and self.device(text="Settings").exists())
    @rule()
    def delete_category_should_remove_immediately(self):
        print("time: " + str(time.time() - start_time))
        category_count = self.device(resourceId="it.feio.android.omninotes:id/count").count
        selected_category_index = random.randint(0, category_count - 1)
        selected_category = self.device(resourceId="it.feio.android.omninotes:id/count")[selected_category_index].left(resourceId="it.feio.android.omninotes:id/title")
        selected_category_name = selected_category.get_text()
        print("selected_category_name: " + selected_category_name)
        time.sleep(1)
        selected_category.long_click()
        time.sleep(1)
        self.device(text="DELETE").click()
        time.sleep(1)
        self.device(text="CONFIRM").click()
        time.sleep(1)
        assert not self.device(text=selected_category_name).exists()
    
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/340/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/340_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
