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
    
    # 6857
    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        self.device(description="More options").exists() and 
        self.device(resourceId="com.ichi2.anki:id/action_search").exists() and 
        self.device(resourceId="com.ichi2.anki:id/card_column2").exists()
    )
    @rule()
    def edit_card_should_remember_scroll_position(self):
        selected_card = self.device(resourceId="com.ichi2.anki:id/card_column2")[0].get_text()
        print("selected_card: " + str(selected_card))
        edit_card = random.choice(self.device(resourceId="com.ichi2.anki:id/card_sfld"))
        edit_card.long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Edit note").click()
        time.sleep(1)
        new_front = st.text(alphabet=string.ascii_letters,min_size=1, max_size=3).example()
        print("new_front: " + str(new_front))
        self.device(resourceId="com.ichi2.anki:id/id_note_editText").set_text(new_front)
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_save").click()
        time.sleep(1)
        assert self.device(resourceId="com.ichi2.anki:id/card_column2")[0].get_text() == selected_card, "scroll position should not change"
start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6857/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/6857_new.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
