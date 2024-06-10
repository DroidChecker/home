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
        self.device.set_fastinput_ime(True)
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

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="Settings").exists() and self.device(resourceId="it.feio.android.omninotes:id/lockedIcon").exists())
    @rule()
    def swipe_locked_note(self):
        print("time: " + str(time.time() - start_time))
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/lockedIcon").up(resourceId="it.feio.android.omninotes:id/note_title")
        selected_note_text = selected_note.get_text()
        print("selected_note_text: " + selected_note_text)
        time.sleep(1)
        selected_note.scroll.horiz.forward(steps=100)
        time.sleep(3)
        self.device.press("recent")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=selected_note_text).exists()


start_time = time.time()


t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/801/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/801.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
