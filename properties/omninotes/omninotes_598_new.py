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
        main_path=None,
        run_initial_rules_after_every_mutation=True
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
            main_path=main_path,
            run_initial_rules_after_every_mutation=run_initial_rules_after_every_mutation
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
        
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="Navigation").click()
        time.sleep(1)
        self.device(text="Group not categorized").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        
        self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        time.sleep(1)
        self.device(text="Text note").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        time.sleep(1)
        
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        self.device(text="ADD CATEGORY").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        # lock note
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Lock").click()
        time.sleep(1)
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
        
    
    @precondition(lambda self: self.device(text="Data").exists() and self.device(text="Password").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="REMOVE PASSWORD").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        # open note
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            print("no note")
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        time.sleep(1)
        assert not self.device(text="PASSWORD FORGOTTEN").exists()
    
    @precondition(lambda self: self.device(description="More options").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def action_lock_a_note(self):
        title = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("title: " + title)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text(title)
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Lock").click()
        time.sleep(1)
        if self.device(text="Insert password").exists():
            self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            time.sleep(1)
            self.device(text="OK").click()
            time.sleep(3)
            self.device.press("back")
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
            time.sleep(3)
            self.device.press("back")
start_time = time.time()


t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/598/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
