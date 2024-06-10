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
        self.device.press("back")

    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/imgvCover").exists() and self.device(resourceId="de.danoeh.antennapod:id/audio_controls").exists()
    )
    @rule()
    def rotate_device_shouldnot_make_cover_disappear(self):
        self.device.set_orientation('l')
        time.sleep(1)
        self.device.set_orientation('n')
        time.sleep(1)
        assert self.device(resourceId="de.danoeh.antennapod:id/imgvCover").exists()

start_time = time.time()

t = Test(
    apk_path="./apk/antennapod/1.7.1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/2992/mutate/1",
    policy_name="mutate",
    timeout=21600,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/2992.json"
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
