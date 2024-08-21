# DroidChecker

DroidChecker is a general and practical testing tool based on the idea of property-based testing for finding functional bugs in Android apps.

## Setup

Requirements:

- Python 3.8+
- Android SDK

```bash
git clone https://github.com/DroidChecker/home
cd home
pip install -e .
```

You can create an emulator before running DroidChecker. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you start using DroidChecker quickly：

```bash
sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
sdkmanager "system-images;android-29;google_apis;x86"
avdmanager create avd --force --name Android10.0 --package 'system-images;android-29;google_apis;x86' --abi google_apis/x86 --sdcard 1024M --device "pixel_2"
```

Next, you can start one emulator and assign their port numbers with the following commands:

```bash
emulator -avd Android10.0 -read-only -port 5554
```

## Getting Started

### Quick example

If you have downloaded our project and configured the environment, you only need to enter "example/" to execute our sample property with the following command:

```
droidchecker -f example.py -a omninotes.apk
```

That's it! You can see the test results in the "output" directory.
You can also find other parameters in ``droidchecker -h``.

### Optional arguments

DroidChecker provides the following options. please consult ``droidchecker -h`` for a full list.

``-f``: The test files that contain the properties.

``-a --apk``: The apk file of the app under test.

``-d --device_serial``: The serial number of the device used in the test. (use 'adb devices' to find)

``-o --output``: The output directory of the execution results.

``-p --policy``: The policy name of the exploration. ("random" or "mutate")

``-t --timeout``: The maximum testing time.

``-n``: Every n events, then restart the app.

``-m --main_path``: the file of the main path.

### Specify your properties

A property in DroiodChecker consists of three parts: A function that looks like a normal test, a `@rule` decorator that specifies this function as a property, and a ``@precondition`` decorator that specifies the precondition of the property.

Here is an example of a property:

```python
@precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists())
@rule()
def search_bar_should_exist_after_rotation(self):
    d.rotate('l')
    d.rotate('n')
    assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 
```

This is an example property from OmniNotes. The property checks if the search exists after rotating the device. The property is defined as a function `search_bar_should_exist_after_rotation`. The function contains the test logic. The `@rule` decorator specifies this function as a property.

Note that we use the `@precondition` decorator to specify the precondition of the property. The precondition is a lambda function that returns a boolean value. If the lambda function returns `True`, the property will be executed. Otherwise, the property will be skipped.

To run this property, we need to define a test class that inherits from ``AndroidCheck``. Then put this property in the test class

Finally, we can run the property by executing the following command:

```bash
droidchecker -f [property_file_name] -a [apk_file_name]

```

where ``property_file_name`` is the name of the property file.

### API Documents



### UI events

Note that currently, we use [uiautomator2](https://github.com/openatx/uiautomator2) to interact with the app. You can find more information in [uiautomator2](https://github.com/openatx/uiautomator2).
You can also use other tools to interact with the app, which can be easily implemented by modifying the `main.py`.

For example, to send the click event to the app, you can use the following code:

```python
d(resourceId="player_playback_button").click()
```

``self.device`` is the object of the uiautomator2.
``resourceId`` sets the resource id of the element.
``click()`` sends the click event to the element.

Here are some common operations:

* click
  ```python
  d(text="OK").click()
  ``` 
* long_click
  ```python
  d(text="OK").long_click()
  ```
* edit text
  ```python
  d(text="OK").set_text("text")
  ```
* rotate device
  ```python
  d.rotate("l") # or left
  d.rotate("r") # or right
  ```
* press [key]
  ```python
  d.press("home")
  d.press("back")
  ```
We use selector to identify the UI object in the current window.  

**Selector**  
(you can also look at [uiautomator2](https://github.com/openatx/uiautomator2?tab=readme-ov-file#selector))  
Selector is a handy mechanism to identify a specific UI object in the current window.  
Selector supports below parameters.

*  `text`, `textContains`, `textMatches`, `textStartsWith`
*  `className`, `classNameMatches`
*  `description`, `descriptionContains`, `descriptionMatches`, `descriptionStartsWith`
*  `checkable`, `checked`, `clickable`, `longClickable`
*  `scrollable`, `enabled`,`focusable`, `focused`, `selected`
*  `packageName`, `packageNameMatches`
*  `resourceId`, `resourceIdMatches`
*  `index`, `instance`  

### initialize
We use ``@initialize`` to pass the welcome page or the login page of the app.
For example, in OmniNotes, we can use ``@initialize`` to specify a function and wrtite the corresponding UI events to pass the welcome page.

```python
@initialize()
def pass_welcome_pages(self):
    # click next button 5 times
    for _ in range(5):
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
    # click done button
    d(resourceId="it.feio.android.omninotes.alpha:id/done").click()
```

The, after testing started, this function will be executed first to pass the welcome page.

### Run multiple properties together
Suppose we have several properties in different files, we can run them together by specifying multiple files in the command line.

```bash
droidchecker -f [property_file_name1] [property_file_name2] -a [apk_file_name]
```

# Acknowledgement

1. [droidbot](https://github.com/honeynet/droidbot)
2. [uiautomator2](https://github.com/openatx/uiautomator2)