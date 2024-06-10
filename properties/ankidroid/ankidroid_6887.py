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

    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/new_number").exists() and 
        self.device(description="More options").exists()
    )
    @rule()
    def add_new_card_should_update_new_card_count(self):
        original_card_count = int(self.device(resourceId="com.ichi2.anki:id/new_number").get_text())
        print("original_card_count: " + str(original_card_count))
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Edit note").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Add note").click()
        time.sleep(1)
        front = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("front: " + str(front))
        self.device(resourceId="com.ichi2.anki:id/id_note_editText").set_text(front)
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_save").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        new_card_count = int(self.device(resourceId="com.ichi2.anki:id/new_number").get_text())
        print("new_card_count: " + str(new_card_count))
        assert new_card_count == original_card_count + 1, "new card count should increase by 1"


start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.12.1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6887/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/6887.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
