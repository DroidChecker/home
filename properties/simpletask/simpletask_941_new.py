import string
import sys
import time
sys.path.append("..")
from droidchecker.main import *

class Test(AndroidCheck):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()


    @initialize()
    def set_up(self):
        d.set_fastinput_ime(True)
        d(text="OK").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        d(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        
        d(text="OK").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 10 and not d(text="Settings").exists() and not d(text="Saved filters").exists())
    @rule()
    def enter_task_and_back_should_keep_position(self):
        task_count = int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = d(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        
        assert d(text=selected_task_name).exists(), "selected_task_name not exists"





t = Test()

setting = Setting(
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/941/1",
    policy_name="random",

)

