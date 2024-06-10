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
        send_document=True,
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
            send_document=send_document,
            main_path=main_path
        )   
    
    @precondition(
        lambda self: self.device(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        self.device(text="Question").exists() and
        self.device(text="Answer").exists() 
    )
    @rule()
    def question_and_answer_should_be_consistent(self):
        card = random.choice(self.device(resourceId="com.ichi2.anki:id/card_item_browser"))
        question = card.child(resourceId="com.ichi2.anki:id/card_sfld").get_text()
        print("question: " + question)
        answer = card.child(resourceId="com.ichi2.anki:id/card_column2").get_text()
        print("answer: " + answer)
        card.click()
        time.sleep(1)
        front_text = self.device(description="Front",resourceId="com.ichi2.anki:id/id_note_editText").get_text()
        back_text = self.device(description="Back",resourceId="com.ichi2.anki:id/id_note_editText").get_text()
        print("front_text: " + str(front_text))
        print("back_text: " + str(back_text))
        assert front_text == question and back_text == answer
        
start_time = time.time()

t = Test(
    apk_path="./apk/ankidroid/2.10.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6167/random_100/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    send_document=False,
    main_path="main_path/ankidroid/6167.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
