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
        
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="Navigation").click()
        time.sleep(1)
        self.device(text="Group not categorized").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device.press("back")

    
    # bug #401
    @precondition(lambda self: self.device(text="Uncategorized").exists() and self.device(text="Settings").exists())
    @rule()
    def rule_uncategory_should_contain_notes(self):
        self.device(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
        time.sleep(1)
        assert self.device(resourceId="it.feio.android.omninotes:id/root").exists()
   
start_time = time.time()


t = Test(
    apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/401/mutate_new/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/401_new.json",
    run_initial_rules_after_every_mutation=False
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
