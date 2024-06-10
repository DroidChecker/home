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
        if self.device(text="OK").exists():
            self.device(text="OK").click()


    @initialize()
    def set_up(self):
        self.device.set_fastinput_ime(True)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        time.sleep(1)
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 10 and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def enter_task_and_back_should_keep_position(self):
        task_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        time.sleep(1)
        assert self.device(text=selected_task_name).exists(), "selected_task_name not exists"


start_time = time.time()


t = Test(
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/941/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
