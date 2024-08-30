import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @initialize()
    def set_up(self):
        d.press("back")

    @precondition(
        lambda self: d(text="Downloads").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/clear_logs_item").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/container").exists()
    )
    @rule()
    def clear_download_log_should_work(self):
        d(resourceId="de.danoeh.antennapod.debug:id/clear_logs_item").click()
        
        assert not d(resourceId="de.danoeh.antennapod.debug:id/container").exists(), "clear log failed"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.1.0-RC1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4656/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4656.json"
)
run_android_check_as_test(t,setting)

