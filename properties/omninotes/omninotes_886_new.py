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
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Trash").exists() and not self.device(text="Settings").exists())
    @rule()
    def rule_trash_note_cannot_be_searched(self):
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        print("selected_note_title: " + selected_note_name)
        selected_note_content = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].sibling(resourceId="it.feio.android.omninotes:id/note_content")
        
        has_content = False
        if selected_note_content.exists():
            selected_note_content = selected_note_content.get_text()
            print("selected_note_content: " + selected_note_content)
            has_content = True
        
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        self.device(text="Notes").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_search").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/search_src_text").set_text(selected_note_name)
        time.sleep(1)
        self.device.send_action("search")
        time.sleep(1)
        if has_content:
            assert not (self.device(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").exists() and self.device(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").sibling(resourceId="it.feio.android.omninotes:id/note_title").get_text() == selected_note_name), "selected_note_content: " + str(selected_note_content)
        else:
            assert not (self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists() and not self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").sibling(resourceId="it.feio.android.omninotes:id/note_content").exists()), "selected_note_name: " + str(selected_note_name)
        print("check list")

        self.device(resourceId="it.feio.android.omninotes:id/menu_uncomplete_checklists").click()
        time.sleep(1)
        if has_content:
            assert not (self.device(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").exists() and self.device(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").sibling(resourceId="it.feio.android.omninotes:id/note_title").get_text() == selected_note_name), "selected_note_content: " + str(selected_note_content)
        else:
            assert not (self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists() and not self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").sibling(resourceId="it.feio.android.omninotes:id/note_content").exists()), "selected_note_name: " + str(selected_note_name)
   
start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/886/mutate_new/1",
    policy_name="mutate",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/886_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
