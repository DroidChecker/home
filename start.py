from droidchecker import input_manager
from droidchecker.main import AndroidCheck, Setting, run_android_check_as_test

import importlib
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Start Droidchecker to test app.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f",nargs="+", action="store",dest="files", help="The python files to be tested.")
    parser.add_argument("-d", action="store", dest="device_serial", default=input_manager.DEFAULT_DEVICE_SERIAL,
                        help="The serial number of target device (use `adb devices` to find)")
    parser.add_argument("-a", action="store", dest="apk_path", required=True,
                        help="The file path to target APK")
    parser.add_argument("-o", action="store", dest="output_dir", default="output",
                        help="directory of output")
    parser.add_argument("-p","--policy", action="store", dest="policy",choices=["random", "mutate"], default=input_manager.DEFAULT_POLICY,
                        help='Policy to use for test input generation. ')
    parser.add_argument("-t", "--timeout", action="store", dest="timeout", default=input_manager.DEFAULT_TIMEOUT, type=int,
                        help="Timeout in seconds. Default: %d" % input_manager.DEFAULT_TIMEOUT)
    parser.add_argument("-n","--number_of_events_that_restart_app", action="store", dest="number_of_events_that_restart_app", default=100, type=int,
                        help="Every xx number of events, then restart the app. Default: 100")
    parser.add_argument("-m", "--main_path", action="store", dest="main_path", default=None)
    options = parser.parse_args()
    return options


def import_and_instantiate_classes(files):
    # 导入文件中的类，并且进行实例化，然后返回实例化的对象
    droidcheck_instance = []
    for file in files:
        print(file)
        module_name = os.path.splitext(file)[0]
        module = importlib.import_module(module_name)

        # 寻找模块中的所有类，并尝试实例化它们
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, AndroidCheck) and attr is not AndroidCheck:
                instance = attr()  # 实例化子类
                droidcheck_instance.append(instance)
    return droidcheck_instance

def main():

    options = parse_args()
    test_classes = []
    if options.files is not None:
        test_classes = import_and_instantiate_classes(options.files)
    setting =  Setting(apk_path=options.apk_path, 
                       device_serial=options.device_serial,
                       output_dir=options.output_dir,
                       timeout=options.timeout,
                       policy_name=options.policy,
                       number_of_events_that_restart_app=options.number_of_events_that_restart_app)

    print(AndroidCheck._rules_per_class)
    run_android_check_as_test(test_classes[0],setting)

if __name__ == "__main__":
    main()
    

    