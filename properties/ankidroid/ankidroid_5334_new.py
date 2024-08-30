import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

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
        send_document=True
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
            send_document=send_document
        )

    @initialize()
    def set_up(self):
        d(text="Get Started").click()

    # 5334
    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/new_number").exists() and
        d(resourceId="com.ichi2.anki:id/answer_field").exists() and 
        d(resourceId="com.ichi2.anki:id/answer_field").get_text() != "Type answer" and
        d(resourceId="com.ichi2.anki:id/answer_options_layout").exists()
    )
    @rule()
    def text_should_display_after_type_answer(self):
        typed_text = d(resourceId="com.ichi2.anki:id/answer_field").get_text()
        print("typed_text: " + typed_text)
        d(resourceId="com.ichi2.anki:id/answer_options_layout").click()
        
        for view in d(resourceId="content").child(className="android.view.View"):
            print("view text: " + view.get_text())
            if typed_text in view.get_text():
                return True 
        assert False, "text should display after type answer"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5334/mutate_new/1",
    policy_name="random",

    main_path="main_path/ankidroid/5334_new.json",
    send_document=False
)

