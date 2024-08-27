Setup
==============

Requirements:
* Python 3.8+
* Android SDK

You need to create an emulator before running DroidChecker. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you start using DroidChecker quickly：

..code:: bash
    sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
    sdkmanager "system-images;android-29;google_apis;x86"
    avdmanager create avd --force --name Android10.0 --package 'system-images;android-29;google_apis;x86' --abi google_apis/x86 --sdcard 1024M --device "pixel_2"


Next, you can start one emulator and assign their port numbers with the following commands:

..code:: bash
    emulator -avd Android10.0 -read-only -port 5554
