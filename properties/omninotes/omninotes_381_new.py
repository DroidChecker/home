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
    
    # bug #381
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(text="Trash").exists() and self.device(resourceId="it.feio.android.omninotes:id/root").exists() and not self.device(text="Settings").exists())
    @rule()
    def restore_note_from_trash_should_work(self):
        print("time: " + str(time.time() - start_time))
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
        time.sleep(1)
        note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        print("note_title: " + note_title)
        time.sleep(1)
        is_archive = selected_note.child(resourceId="it.feio.android.omninotes:id/archivedIcon").exists()
        print("is_archive: " + str(is_archive))
        time.sleep(1)
        selected_note.long_click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_sort").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        if is_archive:
            assert self.device(text="Archive").exists(),"Archive should appear in drawer item"
            time.sleep(1)
            self.device(text="Archive").click()
            assert self.device(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Archive"
        else:
            self.device(text="Notes").click()
            time.sleep(1)
            assert self.device(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Notes"
    
start_time = time.time()
t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/381/mutate_new/1",
    policy_name="mutate",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/381_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
