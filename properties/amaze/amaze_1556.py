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
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(resourceId="com.amaze.filemanager:id/fab_expand_menu_button").exists() and not self.device(resourceId="com.amaze.filemanager:id/design_menu_item_action_area").exists())
    @rule()
    def rule_rename(self):

        print("time: " + str(time.time() - start_time))
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        time.sleep(1)
        self.device(text="Rename").click()
        time.sleep(1)
        new_file_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=5).example()
        print("new file name: "+str(new_file_name))
        self.device(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(new_file_name)
        time.sleep(1)
        self.device(text="SAVE").click()
        time.sleep(1)
        assert not self.device(text=selected_file_name).exists(), "rename failed with new_file_name: " + new_file_name
    

start_time = time.time()

t = Test(
    apk_path="./apk/amaze/amaze-3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1556/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
