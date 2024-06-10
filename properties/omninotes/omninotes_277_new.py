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
        
    
    # bug 277
    @precondition(
            lambda self: 
            self.device(text="Select tag(s)").exists() and 
            self.device(resourceId="android:id/text1").exists() and
            self.device(text="OK").exists()
            )
    @rule()
    def rule_search_by_tag_should_display_results(self):
        
        tag_count = int(self.device(resourceId="android:id/text1").count)
        print("tag_count: " + str(tag_count))
        if tag_count == 0:
            print("no tag, return")
            return
        selected_tag = random.randint(0, tag_count - 1)
        selected_tag_text = self.device(resourceId="android:id/text1")[selected_tag].info['text']
        selected_tag_name = selected_tag_text.rsplit(" ", 1)[0]
        print("selected_tag: " + str(selected_tag_name))
        note_count = selected_tag_text.rsplit(" ", 1)[1].split("(")[1].split(")")[0]
        
        self.device(resourceId="android:id/text1")[selected_tag].click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        if self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists():
            print("wrong page, return")
            return
        if "," in self.device(resourceId="it.feio.android.omninotes:id/search_query").info['text']:
            print("multiple tag, return")
            return
        assert self.device(resourceId="it.feio.android.omninotes:id/root").exists(), "no note"
        assert self.device(resourceId="it.feio.android.omninotes:id/root").count <= int(note_count), "note count < " + str(note_count)
        random.choice(self.device(resourceId="it.feio.android.omninotes:id/note_title")).click()
        time.sleep(1)
        assert self.device(text=selected_tag_name).exists(), "no tag"

        
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/277/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/277_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
