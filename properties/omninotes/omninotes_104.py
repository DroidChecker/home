import string
import sys
import time
from droidchecker.main import *

class Test(AndroidCheck):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
        
        if d(text="Not now").exists():
            d(text="Not now").click()
        
        

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def remove_password_should_not_affect_notes(self):
        print("time: " + str(time.time() - start_time))
        note_title = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("title: " + note_title)
        d(resourceId="it.feio.android.omninotes:id/detail_title").set_text(note_title)
        
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("content: " + content)
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text(content)
        
        d(description="More options").click()
        
        d(text="Mask").click()
        
        if d(resourceId="it.feio.android.omninotes:id/password").exists():
            d(resourceId="it.feio.android.omninotes:id/password").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/question").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
            
            d(text="Confirm").click()
            time.sleep(2)
            d.press("back")
            
            d.press("back")
        else:
            d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            
            d(text="Confirm").click()
        time.sleep(2)
        d.press("back")

        
        d(text="Notes").click()
        
        d(text="SETTINGS").click()
        
        d(text="Data").click()
        
        d(text="Password").click()
        
        d(text="Confirm").click()
        
        if not d(text="Insert password").exists():
            print("password is not set, return")
            return 
        d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        
        d(text="Confirm").click()
        
        d(text="Confirm").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        assert d(text=note_title).exists()," note title should exists the same as before "+note_title
        assert d(text=content).exists()," note content should exists the same as before "+content




t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-4.7.2.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/104/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/104.json"
)
run_android_check_as_test(t,setting)

