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
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_share").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_tag").exists()  )
    @rule()
    def count_char_in_note(self):
        title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + str(title))
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + str(content))
        if content == "Content":
            content = ""
        if title == "Title":
            title = ""
        import re
        number_of_char = len(re.findall(".",str(title))) + len(re.findall(".",str(content)))
        print("number of char: " + str(number_of_char))
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Info").click()
        time.sleep(1)
        chars = int(self.device(resourceId="it.feio.android.omninotes:id/note_infos_chars").get_text())
        print("chars calculated by omninotes: " + str(chars))
        time.sleep(1)
        assert number_of_char == chars

start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/800/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/800.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
