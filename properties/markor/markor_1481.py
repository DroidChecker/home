import string
from main import *
import time
import sys
import re

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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Date").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Reverse order").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Folder first").click()
        
    
    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_rename_file(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        is_file = True
        if "." not in file_name:
            is_file = False
            print("not a file")
            return
        file_name_suffix = file_name.split(".")[-1]
        print("file name: "+str(file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        if is_file:
            name = name+"."+file_name_suffix
        print("new file name: "+str(name))
        self.device(resourceId="net.gsantner.markor:id/new_name").set_text(name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        assert self.device(resourceId="net.gsantner.markor:id/ui__filesystem_dialog__list").child_by_text(name,allow_scroll_search=True).exists()


start_time = time.time()

# args = sys.argv[1:]
# apk_path = args[0]
# device_serial = args[1]
# output_dir = args[2]
# xml_path = args[3]
# main_path_path = args[4]
# source_activity = args[5]
# target_activity = args[6]
# policy_name = args[7]
# t = Test(
#     apk_path="./apk/AnkiDroid-2.15.2.apk",
#     device_serial="emulator-5554",
#     output_dir="output/anki/random2",
#     event_count=1000,
#     xml_path="./xml_graph/Anki_CTG.xml",
#     source_activity="DeckPicker",
#     target_activity="Preferences",
#     policy_name="random", dfs_greedy
# )
t = Test(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1481/random_10/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 10
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
