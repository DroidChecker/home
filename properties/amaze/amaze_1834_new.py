import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @precondition(lambda self: d(textContains=".zip").exists() and not d(text="Internal Storage").exists() and not d(resourceId="com.amaze.filemanager:id/donate").exists() and not d(text="Cloud Connection").exists() and not d(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def extract_zip_file_shouldnot_need_password(self):
        print("time: " + str(time.time() - start_time))
        zip_file = d(textContains=".zip")
        folder_name = zip_file.get_text().split(".")[0]
        print("zip_file: "+str(zip_file.get_text()))
        zip_file.click()
        
        d(text="EXTRACT").click()
        
        assert d(resourceId="com.amaze.filemanager:id/listView").child_by_text(folder_name,allow_scroll_search=True,resourceId="com.amaze.filemanager:id/firstline").exists(), "extract zip file failed with zip file name: "+str(zip_file.get_text())



t = Test()

setting = Setting(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1834/1",
    policy_name="random",

)

