import os
import random
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Union,
    overload,
)
import traceback
import attr
import uiautomator2 as u2
from droidchecker import env_manager, input_manager
from droidchecker.droidbot import DroidBot
import inspect
from copy import copy
from uiautomator2.exceptions import UiObjectNotFoundError
import time
from hypothesis.errors import NonInteractiveExampleWarning
import warnings

warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)

RULE_MARKER = "tool_rule"
INITIALIZE_RULE_MARKER = "tool_initialize_rule"
PRECONDITIONS_MARKER = "tool_preconditions"
INVARIANT_MARKER = "tool_invariant"


@attr.s()
class Rule:
    function = attr.ib()
    preconditions = attr.ib()


def rule() -> Callable:
    def accept(f):
        precondition = getattr(f, PRECONDITIONS_MARKER, ())
        rule = Rule(function=f, preconditions=precondition)

        def rule_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(rule_wrapper, RULE_MARKER, rule)
        return rule_wrapper

    return accept


def precondition(precond: Callable[[Any], bool]) -> Callable:
    def accept(f):
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = getattr(f, RULE_MARKER, None)
        if rule is not None:
            new_rule = attr.evolve(rule, preconditions=rule.preconditions + (precond,))
            setattr(precondition_wrapper, RULE_MARKER, new_rule)
        else:
            setattr(
                precondition_wrapper,
                PRECONDITIONS_MARKER,
                getattr(f, PRECONDITIONS_MARKER, ()) + (precond,),
            )
        return precondition_wrapper

    return accept


def initialize():
    '''
    An initialize decorator behaves like a rule, but all ``@initialize()`` decorated
    methods will be called before any ``@rule()`` decorated methods, in an arbitrary
    order.  Each ``@initialize()`` method will be called exactly once per run, unless
    one raises an exception.
    '''

    def accept(f):
        def initialize_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = Rule(function=f, preconditions=())
        setattr(initialize_wrapper, INITIALIZE_RULE_MARKER, rule)
        return initialize_wrapper

    return accept


class AndroidCheck(object):
    _rules_per_class: Dict[type, List[classmethod]] = {}
    _initializers_per_class: Dict[type, List[classmethod]] = {}

    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        main_path=None,
        is_emulator=True,
        policy_name=input_manager.DEFAULT_POLICY,
        random_input=True,
        script_path=None,
        event_interval=input_manager.DEFAULT_EVENT_INTERVAL,
        timeout=input_manager.DEFAULT_TIMEOUT,
        event_count=input_manager.DEFAULT_EVENT_COUNT,
        cv_mode=None,
        debug_mode=None,
        keep_app=None,
        keep_env=None,
        profiling_method=None,
        grant_perm=True,
        send_document=True,
        enable_accessibility_hard=None,
        master=None,
        humanoid=None,
        ignore_ad=None,
        replay_output=None,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
        run_initial_rules_after_every_mutation=True
    ):
        self.apk_path = apk_path
        self.device_serial = device_serial
        
        self.droidbot = DroidBot(
            app_path=apk_path,
            device_serial=device_serial,
            is_emulator=is_emulator,
            output_dir=output_dir,
            env_policy=env_manager.POLICY_NONE,
            policy_name=policy_name,
            random_input=random_input,
            script_path=script_path,
            event_interval=event_interval,
            timeout=timeout,
            event_count=event_count,
            cv_mode=cv_mode,
            debug_mode=debug_mode,
            keep_app=keep_app,
            keep_env=keep_env,
            profiling_method=profiling_method,
            grant_perm=grant_perm,
            send_document=send_document,
            enable_accessibility_hard=enable_accessibility_hard,
            master=master,
            humanoid=humanoid,
            ignore_ad=ignore_ad,
            replay_output=replay_output,
            android_check=self,
            main_path=main_path,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
            run_initial_rules_after_every_mutation=run_initial_rules_after_every_mutation
        )
        self.device = u2.connect(self.device_serial)
        # disable keyboard
        self.device.set_fastinput_ime(True)
        self.device.implicitly_wait(5)  # set default element wait timeout = 5 seconds
        self._initialize_rules_to_run = copy(self.initialize_rules())
        if not self.rules():
            raise Exception(f"Type {type(self).__name__} defines no rules")
        self.current_rule = None
        self.execute_event = None

    def start(self):
        try:
            self.droidbot.start()
        except Exception:
            traceback.print_exc()

    @classmethod
    def initialize_rules(cls):
        try:
            return cls._initializers_per_class[cls]
        except KeyError:
            pass

        cls._initializers_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, INITIALIZE_RULE_MARKER, None)
            if r is not None:
                cls._initializers_per_class[cls].append(r)
        return cls._initializers_per_class[cls]

    @classmethod
    def rules(cls):
        try:
            return cls._rules_per_class[cls]
        except KeyError:
            pass

        cls._rules_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, RULE_MARKER, None)
            if r is not None:
                cls._rules_per_class[cls].append(r)
        return cls._rules_per_class[cls]

    def execute_initializers(self):
        for initializer in self._initialize_rules_to_run:
            initializer.function(self)

    def execute_rules(self, rules):
        '''random choose a rule, if the rule has preconditions, check the preconditions.
        if the preconditions are satisfied, execute the rule.'''
        '''

        0: assertion error
        1: check property pass
        2: UiObjectNotFoundError
        3: don't need to check property,because the precondition is not satisfied
        '''
        
        if len(rules) == 0:
            return 3
        rule_to_check = random.choice(rules)
        self.current_rule = rule_to_check
        return self.execute_rule(rule_to_check)

    def execute_rule(self, rule):
        if len(rule.preconditions) > 0:
            if not all(precond(self) for precond in rule.preconditions):
                return 3
        # try to execute the rule and catch the exception if assertion error throws
        result = 1
        try:
            time.sleep(1)
            result = rule.function(self)
            time.sleep(1)
        except UiObjectNotFoundError as e:
            print("Could not find the UI object. "+str(e))
            return 2
        except AssertionError as e:
            print("Assertion error. "+str(e))
            return 0
        finally:
            result = 1

        return result

    def get_rules_that_pass_the_preconditions(self) -> List:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        rules_to_check = self.rules()
        rules_meeting_preconditions = []
        for rule_to_check in rules_to_check:
            if len(rule_to_check.preconditions) > 0:
                if all(precond(self) for precond in rule_to_check.preconditions):
                    rules_meeting_preconditions.append(rule_to_check)
        return rules_meeting_preconditions

    def get_rules_without_preconditions(self):
        '''Return the list of rules that do not have preconditions.'''
        rules_to_check = self.rules()
        rules_without_preconditions = []
        for rule_to_check in rules_to_check:
            if len(rule_to_check.preconditions) == 0:
                rules_without_preconditions.append(rule_to_check)
        return rules_without_preconditions

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.
        Does nothing by default.
        """
        ...


from uiautomator2._selector import Selector, UiObject
from uiautomator2 import Device


class Mobile(Device):
    
    def __init__(self,serial, delay=1) -> None:
        super().__init__(serial=serial)
        self.delay = delay

    def __call__(self, **kwargs: Any) -> Any:
        return Ui(self, Selector(**kwargs))

    def rotate(self, mode: str):
        super().set_orientation(mode)
        time.sleep(self.delay)

    def press(self, key: Union[int, str], meta=None):
        super().press(key, meta)
        time.sleep(self.delay)


class Ui(UiObject):

    def click(self, timeout=None, offset=None):
        super().click(timeout, offset)
        time.sleep(self.session.delay)

    def long_click(self, duration: float = 0.5, timeout=None):
        super().long_click(duration, timeout)
        time.sleep(self.session.delay)
    
    def set_text(self, text, timeout=None):
        super().set_text(text, timeout)
        time.sleep(self.session.delay)

    def child(self, **kwargs):
        return Ui(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return Ui(self.session, self.selector.clone().sibling(**kwargs))
    
    
d = Mobile(serial="emulator-5554")




