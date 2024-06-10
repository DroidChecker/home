import string
import sys
import time
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
        if self.device(text="Not now").exists():
            self.device(text="Not now").click()
        time.sleep(1)
        

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def remove_password_should_not_affect_notes(self):
        print("time: " + str(time.time() - start_time))
        note_title = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("title: " + note_title)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text(note_title)
        time.sleep(1)
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("content: " + content)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text(content)
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Mask").click()
        time.sleep(1)
        if self.device(resourceId="it.feio.android.omninotes:id/password").exists():
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
            self.device(text="Confirm").click()
            time.sleep(2)
            self.device.press("back")
            time.sleep(1)
            self.device.press("back")
        else:
            self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            time.sleep(1)
            self.device(text="Confirm").click()
        time.sleep(2)
        self.device.press("back")

        time.sleep(1)
        self.device(text="Notes").click()
        time.sleep(1)
        self.device(text="SETTINGS").click()
        time.sleep(1)
        self.device(text="Data").click()
        time.sleep(1)
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        if not self.device(text="Insert password").exists():
            print("password is not set, return")
            return 
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=note_title).exists()," note title should exists the same as before "+note_title
        assert self.device(text=content).exists()," note content should exists the same as before "+content

start_time = time.time()


t = Test(
    apk_path="./apk/omninotes/OmniNotes-4.7.2.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/104/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/104.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
