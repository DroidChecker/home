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
        self.device(text="Get Started").click()

    # 5352
    @precondition(
        lambda self: self.device(text="Manage note types").exists() and 
        self.device(resourceId="com.ichi2.anki:id/note_type_add").exists() and
        self.device(resourceId="com.ichi2.anki:id/note_name").exists()
    )
    @rule()
    def note_type_should_be_consistent(self):
        self.device(resourceId="com.ichi2.anki:id/note_name").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_add_new_model").click()
        time.sleep(1)
        type_name = st.text(alphabet=string.printable,min_size=1, max_size=6).example()
        print("type_name: " + str(type_name))
        self.device(className="android.widget.EditText").set_text(type_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        assert self.device(resourceId="com.ichi2.anki:id/note_type_editor_fields").child_by_text(type_name, allow_scroll_search=True).exists, "new note type should be added"

start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5352/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/5352_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
