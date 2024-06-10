import string
import sys
import time
import re
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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
            time.sleep(1)
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
    
    def check_hash_tag_exist(self):
        
        for content in self.device(resourceId="it.feio.android.omninotes:id/note_content"):
            content = content.get_text()
            if "#" not in content:
                continue
            matches = re.findall(r'#(\w+)', content) 
            tags = [m for m in matches if content.find("#"+m)==0 or content[content.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            return True
        
        for title in self.device(resourceId="it.feio.android.omninotes:id/note_title"):
            title = title.get_text()
            if "#" not in title:
                continue
            matches = re.findall(r'#(\w+)', title) 
            tags = [m for m in matches if title.find("#"+m)==0 or title[title.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            return True
        
        return False



    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_content").exists() and not
                  self.device(text="SETTINGS").exists() and 
                  self.check_hash_tag_exist() and not
                  self.device(resourceId="it.feio.android.omninotes:id/action_mode_close_button").exists()
    )
    @rule()
    def hash_tag_with_number_start_shouldbe_recognized(self):
        
        hashtag_UI_element = []
        for note_content in self.device(resourceId="it.feio.android.omninotes:id/note_content"):
            content = note_content.get_text()
            if "#" not in content:
                continue
            matches = re.findall(r'#(\w+)', content) 
            print("matches: " + str(matches))
            tags = [m for m in matches if content.find("#"+m)==0 or content[content.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            hashtag = tags
            hashtag_UI_element.append((note_content,hashtag))
        
        for note_title in self.device(resourceId="it.feio.android.omninotes:id/note_title"):
            title = note_title.get_text()
            if "#" not in title:
                continue
            matches = re.findall(r'#(\w+)', title) 
            print("matches: " + str(matches))
            tags = [m for m in matches if title.find("#"+m)==0 or title[title.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            hashtag = tags
            hashtag_UI_element.append((note_title,hashtag))
        
        selected = random.choice(hashtag_UI_element)
        selected_hashtag_UI_element =selected[0]
        selected_hashtag = selected[1]
        selected_hashtag_UI_element.click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        time.sleep(1)
        for tag in selected_hashtag:
            assert self.device(resourceId="it.feio.android.omninotes:id/title",textContains=tag).exists(), "tag not found"

start_time = time.time()

t = Test(
    apk_path="./apk/omninotes/OmniNotes-5.1.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/237/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
