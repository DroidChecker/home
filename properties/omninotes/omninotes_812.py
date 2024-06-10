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
        if not self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").exists() and self.device(description="drawer open").exists():
            self.device(description="drawer open").click()
            time.sleep(1)
            self.device(text="Notes").click()
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
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() and self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="SETTINGS").exists())
    @rule()
    def rule_restore_backup_shouldnot_change_note(self):
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
        has_content = False
        if selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").exists():
            has_content = True
            note_content = selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
            print("note_content: " + note_content)
        time.sleep(1)
        has_attachment = selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists()
        print("has_attachment: " + str(has_attachment))
        
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        self.device(text="SETTINGS").click()
        time.sleep(1)
        self.device(text="Data").click()
        time.sleep(1)
        self.device(text="Sync and Backups").click()
        time.sleep(1)
        self.device(text="Backup").click()
        time.sleep(1)
        back_up_name = self.device(resourceId="it.feio.android.omninotes:id/export_file_name").get_text()
        self.device(text="CONFIRM").click()
        time.sleep(1)
        self.device(text="Restore or delete backups").click()
        time.sleep(1)
        self.device(text=back_up_name).click()
        time.sleep(1)
        self.device(text="CONFIRM").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        
        assert selected_note.exists(), "selected note not exists"
        if note_title is not None:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text() == note_title, "note_title: "  + selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        if has_content:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text() == note_content, "note_content: " + selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
        assert selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists() == has_attachment, "has_attachment: " + str(selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists())


start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/812/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/812.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
