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
        lambda self: self.device(text="Add").exists() and 
        self.device(text="Get shared decks").exists() 
    )
    @rule()
    def cloze_should_work(self):
        self.device(text="Add").click()
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/note_type_spinner").click()
        time.sleep(1)
        self.device(text="Cloze").click()
        time.sleep(1)
        text = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example() + "{{c1::cloze}}"
        self.device(description="Text").set_text(text)
        time.sleep(1)
        self.device(resourceId="com.ichi2.anki:id/action_preview").click()
        time.sleep(1)
        assert not self.device(text="help").exists, "help shouldnot exist"

start_time = time.time()


t = Test(
    apk_path="./apk/ankidroid/2.12.0beta6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6684/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/ankidroid/6684.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
