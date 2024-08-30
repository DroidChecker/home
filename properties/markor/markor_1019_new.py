import string
from droidchecker.main import *
import time
import sys
import re

class Test(AndroidCheck):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        

        
    # 1019
    @precondition(
        lambda self: 
        d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__description").exists() and 
        d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__description").get_text() != "/storage/emulated/0/Documents"
        )
    @rule()
    def rotate_device_should_not_change_the_title(self):
        title = d(resourceId="net.gsantner.markor:id/toolbar").child(className="android.widget.TextView").get_text()
        print("title: "+str(title))
        assert title != "Markor", "title should not be markor"



t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1019/mutate/1",
    policy_name="random",

    main_path="main_path/markor/1019_new.py"
)

