import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(text="App Manager").exists() and 
                  d(description="More options").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def click_sort_should_work(self):
        print("time: " + str(time.time() - start_time))
        d(resourceId="com.amaze.filemanager.debug:id/sort").click()
        
        
        assert d(text="Sort By").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-9c8048a.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2498/mutate/1",
    policy_name="random",

    main_path="main_path/amaze/2498.json"
)
run_android_check_as_test(t,setting)

