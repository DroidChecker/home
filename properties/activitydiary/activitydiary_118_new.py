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

    @precondition(
        lambda self: self.device(text="Diary").exists() and self.device(resourceId="de.rampro.activitydiary:id/picture").exists()
    )
    @rule()
    def delete_pics_should_work(self):
        pic_count = self.device(resourceId="de.rampro.activitydiary:id/picture").count
        print("pic count: " + str(pic_count))
        # random select a pic
        random_index = random.randint(0, pic_count - 1)
        selected_pic = self.device(resourceId="de.rampro.activitydiary:id/picture")[random_index]
        selected_pic_name = selected_pic.up(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("selected pic name: " + selected_pic_name)
        time.sleep(1)
        selected_pic.long_click()
        time.sleep(2)
        self.device(text="OK").click()
        time.sleep(1)
        after_pic_count = self.device(resourceId="de.rampro.activitydiary:id/picture").count 
        print("after pic count: " + str(after_pic_count))
        assert after_pic_count == pic_count - 1, "pic not deleted"
        for i in range(after_pic_count):
            pic_name = self.device(resourceId="de.rampro.activitydiary:id/picture")[i].up(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
            assert pic_name != selected_pic_name, "pic not deleted "+pic_name+" "+selected_pic_name

start_time = time.time()

t = Test(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/118/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
