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

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text() != "Title")
    @rule()
    def remove_password_should_not_affect_notes(self):
        print("time: " + str(time.time() - start_time))
        note_title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + str(note_title))
        time.sleep(1)
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + str(content))
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        if self.device(text="Lock").exists():
            self.device(text="Lock").click()
            time.sleep(1)
            if self.device(resourceId="it.feio.android.omninotes:id/password_request").exists():
                self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
                time.sleep(1)
                self.device(text="OK").click()
            else:    
                self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
                time.sleep(1)
                self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
                time.sleep(1)
                self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
                time.sleep(1)
                self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
                time.sleep(1)
                self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
                time.sleep(1)
                self.device(scrollable=True).fling()
                time.sleep(1)
                self.device(text="OK").click()
                time.sleep(2)
                self.device.press("back")
            
        else:
            print("the note has been lock, return")
            self.device(text="Unlock").click()
            return
        time.sleep(2)
        self.device.press("back")

        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="Data").click()
        time.sleep(1)
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="REMOVE PASSWORD").click()
        time.sleep(1)
        if not self.device(text="Insert password").exists():
            print("password is not set, return")
            return 
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(2)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=note_title).exists()," note title should exists the same as before "+str(note_title)
        self.device(text=note_title).click()
        time.sleep(1)
        assert str(self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()) == content," note content should exists the same as before "+str(content)
        self.device.press("back")

start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/104/mutate_new/1",
    policy_name="mutate",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/104_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
