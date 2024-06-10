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
        
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/search_query").exists() and self.device(resourceId="it.feio.android.omninotes:id/root").exists() and not self.device(text="SETTINGS").exists())
    @rule()
    def search_result_should_not_contain_other_notes(self):
        print("time: " + str(time.time() - start_time))
        text = self.device(resourceId="it.feio.android.omninotes:id/search_query").get_text().split(" ")[1]
        print("search text: " + text)
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note_number = random.randint(0, note_count - 1)
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/root")[selected_note_number]
        print("selected_note: " + str(selected_note_number))
        selected_note.click()
        title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + title)
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + content)
        assert text.lower() in title.lower() or text in content.lower()
    
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-5.2.15.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/283/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/283.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
