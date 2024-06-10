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
        # 打开设置-在navigation 中显示没有被分类的Notes
        # self.device(description="drawer open").click()
        # time.sleep(1)
        # self.device(text="SETTINGS").click()
        # time.sleep(1)
        # self.device(text="Navigation").click()
        # time.sleep(1)
        # self.device(text="Group not categorized").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device.press("back")
        # time.sleep(1)
        # # 创建一个新的Note
        # self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        # time.sleep(1)
        # self.device(text="Text note").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        # time.sleep(1)
        # # 添加新的category
        # self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/buttonDefaultPositive").click()
        # time.sleep(1)
        # category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        # self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(1)
        # # lock note
        # self.device(description="More options").click()
        # time.sleep(1)
        # self.device(text="Lock").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        # time.sleep(1)
        # self.device(scrollable=True).fling()
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(2)
        # self.device.press("back")
        
    
    @precondition(lambda self: self.device(text="Insert password").exists() and self.device(text="PASSWORD FORGOTTEN").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):
        
        self.device(text="OK").click()
        time.sleep(1)
        if self.device(text="Insert password").exists():
            print("wrong password")
            return
        self.device(text="OK").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert not self.device(resourceId="it.feio.android.omninotes:id/lockedIcon").exists()
    
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
    apk_path="./apk/omninotes/OmniNotes-5.5.3.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/598/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
