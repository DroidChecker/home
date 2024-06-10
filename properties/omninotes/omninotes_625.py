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
        
    
    @precondition(lambda self: self.device(text="Categorize as").exists())
    @rule()
    def rule_add_category_should_change_number(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="ADD CATEGORY").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        print("category_name: " + category_name)
        time.sleep(1)
        #assert self.device(resourceId="it.feio.android.omninotes.alpha:id/md_contentRecyclerView").child_by_text(category_name,allow_scroll_search=True).exists()
        if not self.device(text=category_name).exists():
            if self.device(scrollable=True).exists():
                print("scroll to category_name: " + category_name)
                self.device(scrollable=True).scroll.to(text=category_name)
        assert self.device(text=category_name).exists(), "category_name: " + category_name
        # assert self.device(text=category_name).exists(), "category_name: " + category_name
        time.sleep(1)
        assert self.device(text=category_name).right(resourceId="it.feio.android.omninotes:id/count").get_text() == "1", "category_name: " + category_name
    
start_time = time.time()


t = Test(
    apk_path="./apk/omninotes/OmniNotes-5.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/625/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/omninotes/625.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
