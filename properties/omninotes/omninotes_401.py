import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

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
        main_path=None,
        run_initial_rules_after_every_mutation=True
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
            main_path=main_path,
            run_initial_rules_after_every_mutation=run_initial_rules_after_every_mutation
        )

    @initialize()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        # 打开设置-在navigation 中显示没有被分类的Notes
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        
        d.press("back")
        time.sleep(2)
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        if not d(text="SETTINGS").exists():
            d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        d(text="SETTINGS").click()
        
        d(text="Navigation").click()
        
        d(text="Group not categorized").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
    
    @precondition(lambda self: d(text="Uncategorized").exists() and d(text="SETTINGS").exists())
    @rule()
    def rule_uncategory_should_contain_notes(self):
        d(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/root").exists()
        



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/401/random_100/1",
    policy_name="random",

    main_path="main_path/omninotes/401.json",
    run_initial_rules_after_every_mutation=False
)

