# Replication Package

This repository contains all the artifacts (including the source code of DroidChecker, the defined properties, and the APK files of all app subjects) in our paper.

## Directory Structure

    important files and directories in the replication package are as follows:

    |

    |--- apk:                            The apk files of 8 apps used in our experiment

    |--- droidbot:                       The source code of DroidChecker, which focuses on generating test inputs
        |
        |--- input_policy:               The random exploration strategy and main path guided exploration strategy
        |
    |--- properties:                     The defined properties for all the apps

    |--- main.py:                        The source code of DroidChecker, which focuses on parsing properties

## DroidChecker

DroidChecker is a general and practical testing tool based on the idea of property-based testing for finding functional bugs in Android apps.

### Download

```

git clone https://github.com/DroidChecker/home

```

### Environment

If your system has the following support, you can directly run DroidChecker.

- Android SDK
- Python 3.8+

We use some Python libraries, you can install them by running the following command:

```
pip install -t requirements.txt
```

### Setting up

You can create an emulator before running DroidChecker. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you start using DroidChecker quickly：

```
sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
sdkmanager "system-images;android-29;google_apis;x86"
avdmanager create avd --force --name Android10.0 --package 'system-images;android-29;google_apis;x86' --abi google_apis/x86 --sdcard 1024M --device "pixel_2"
```

Next, you can start one emulator and assign their port numbers with the following commands:

```
emulator -avd Android10.0 -read-only -port 5554
```

### Run

#### run existing properties

If you have downloaded our project and configured the environment, you only need to enter "download_path/" to execute our sample property with the following command:

```
python -m properties.omninotes.omninotes_888
```

We set the arguments of this sample property in the corresponding file, and you can read the corresponding property file in the "properties" directory to understand the property you are running.

The arguments of the property,

``apk_path``: the file path of APK

``device_serial``: the serial number of devices used in the test, which can be obtained by executing "adb devices" in the terminal.

``output_dir``: the output directory of the execution results.

``policy_name`` The policy name of the exploration.

``timeout`` The maximum running time.

``number_of_events_that_restart_app`` The number of events in per round of test.

### Specify your properties

A property in DroiodChecker consists of three parts: A function that looks like a normal test, a `@rule` decorator that specifies this function as a property, and a ``@precondition`` decorator that specifies the precondition of the property.

Here is an example of a property:

```python
    @precondition(
        lambda self: self.device(resourceId="player_playback_button").exists()
    )
    @rule()
    def station_name_should_be_consistent(self):
        station_name = self.device(resourceId="player_station_name").get_text()
        self.device(resourceId="player_playback_button").click()
        time.sleep(1)
        assert self.device(resourceId="player_station_name",text=station_name).exists()

```

This is an example property from transistor. The property checks if the station name is consistent after clicking the playback button. The property is defined as a function `station_name_should_be_consistent`. The function contains the test logic. The `@rule` decorator specifies this function as a property.


Note that we use the `@precondition` decorator to specify the precondition of the property. The precondition is a lambda function that returns a boolean value. If the lambda function returns `True`, the property will be executed. Otherwise, the property will be skipped.

To run this property, we need to define a test class that inherits from ``AndroidCheck``. Then put this property in the test class and define the arguments of the property in the test class. Like the property defined in the ``properties`` directory.

Finally, we can run the property by executing the following command:

```

python -m [property_file_name]

```
where ``property_file_name`` is the name of the property file.

### API Documents

Note that currently, we use [uiautomator2](https://github.com/openatx/uiautomator2) to interact with the app. You can find more information in [uiautomator2](https://github.com/openatx/uiautomator2).
You can also use other tools to interact with the app, which can be easily implemented by modifying the `AndroidCheck` class.

For example, to send the click event to the app, you can use the following code:

```python
self.device(resourceId="player_playback_button").click()
```

```self.device``` is the object of the uiautomator2.
```resourceId``` sets the resource id of the element.
```click()``` sends the click event to the element.
