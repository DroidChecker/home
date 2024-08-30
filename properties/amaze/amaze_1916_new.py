import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    
        self.add_file_names = []
    

    @precondition(lambda self: d(text="Documents").exists()  and not d(text="Settings").exists())
    @rule()
    def rule_documnets(self):
        print("time: " + str(time.time() - start_time))
        
        assert d(resourceId="com.amaze.filemanager:id/firstline").exists()



t = Test()

setting = Setting(
    apk_path="./apk/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1916/1",
    policy_name="random",

)

