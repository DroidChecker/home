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
        lambda self: self.device(text="Settings").exists() and 
        self.device(text="Search…").exists() 
    )
    @rule()
    def notification_priority_should_display_in_setting(self):
        texts = st.text(alphabet=string.ascii_letters,min_size=1, max_size=4).example()
        print("text: " + texts)
        self.device(text="Search…").set_text(texts)
        time.sleep(1)
        if not self.device(resourceId="android:id/title").exists():
            print("title not found")
            return
        random_select_title = random.choice(self.device(resourceId="android:id/title"))
        title = str(random_select_title.get_text())
        print("random_select_title: " + title)
        time.sleep(1)
        random_select_title.click()
        time.sleep(1)
        assert self.device(text=title).exists(), "title not found "+str(title)
start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4640/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
