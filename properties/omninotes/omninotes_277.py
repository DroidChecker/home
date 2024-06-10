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
        self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        
    
    @precondition(
            lambda self: 
            self.device(text="Search in notes").exists() and 
            self.device(resourceId="it.feio.android.omninotes:id/menu_tags").exists() and not 
            self.device(text="Settings").exists()
            )
    @rule()
    def rule_search_by_tag_should_display_results(self):
        self.device(resourceId="it.feio.android.omninotes:id/menu_tags").click()
        time.sleep(1)
        tag_count = int(self.device(resourceId="it.feio.android.omninotes:id/control").count)
        print("tag_count: " + str(tag_count))
        if tag_count == 0:
            print("no tag, return")
            return
        selected_tag = random.randint(0, tag_count - 1)+1
        selected_tag_name = self.device(resourceId="it.feio.android.omninotes:id/title")[selected_tag].info['text']
        print("selected_tag: " + str(selected_tag_name))
        note_count = selected_tag_name.rsplit(" ", 1)[1].split("(")[1].split(")")[0]
        self.device(resourceId="it.feio.android.omninotes:id/title")[selected_tag].click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        assert self.device(resourceId="it.feio.android.omninotes:id/root").exists(), "no note"
        assert self.device(resourceId="it.feio.android.omninotes:id/root").count <= int(note_count), "note count < " + str(note_count)
    
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/5.2.10.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/277/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
