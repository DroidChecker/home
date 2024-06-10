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
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @initialize()
    def set_up(self):
        pass

    @precondition(
        lambda self: self.device(text="Edit note").exists() and
        self.device(resourceId="com.ichi2.anki:id/CardEditorTagText").exists() and
        len(self.device(resourceId="com.ichi2.anki:id/CardEditorTagText").get_text())>=7
    )
    @rule()
    def filter_by_tag(self):
        tag_info = self.device(resourceId="com.ichi2.anki:id/CardEditorTagText").get_text()
        tag_list = tag_info[6:].split(", ")
        tag_name = random.choice(tag_list)
        print("tag_name: "+tag_name)
        deck_name = self.device(resourceId="com.ichi2.anki:id/CardEditorDeckText").right(resourceId="android:id/text1").get_text()
        print("deck_name: "+deck_name)
        front = self.device(resourceId="com.ichi2.anki:id/id_note_editText",description="Front").get_text()
        print("front: "+front)
        time.sleep(1)
        
        self.device(resourceId="com.ichi2.anki:id/action_save").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Filter by tag").click()
        time.sleep(1)
        self.device(text=tag_name).click()
        time.sleep(1)
        self.device(text="SELECT").click()
        time.sleep(1)
        assert self.device(resourceId="com.ichi2.anki:id/card_sfld").exists(), "card not found"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.12.1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7070/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
