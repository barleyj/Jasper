from jasper.utility import extract_traceback
from termcolor import colored
import textwrap


class Display(object):

    def __init__(self):
        self.display_string = ''
        self.indentation_level = 0

    def display(self):
        print(self.display_string)

    @staticmethod
    def cyan(text):
        return colored(text, 'cyan')

    @staticmethod
    def magenta(text):
        return colored(text, 'magenta')

    @staticmethod
    def yellow(text):
        return colored(text, 'yellow')

    @staticmethod
    def red(text):
        return colored(text, 'red')

    @staticmethod
    def grey(text):
        return colored(text, 'white')

    @staticmethod
    def indent(text, amount):
        return textwrap.indent(text, ' ' * amount)

    def __push_to_display(self, display_string):
        self.display_string += self.indent(display_string + '\n', self.indentation_level)

    def prepare_suite(self, suite):
        color = self.cyan if suite.passed else self.red

        self.__push_to_display(self.prepare_border(color, 150))
        for feature in suite.features:
            self.prepare_feature(feature)
        self.__push_to_display(self.prepare_border(color, 150))
        self.prepare_statistics(suite)
        self.__push_to_display(self.prepare_border(color, 150))

    def prepare_feature(self, feature):
        color = self.cyan if feature.passed else self.red

        self.__push_to_display(self.prepare_border(color, 150))
        self.__push_to_display(color(f'Feature: {feature.description}'))

        self.indentation_level += 4
        if feature.before_each is not None:
            for before_each in feature.before_each:
                self.prepare_before_each(before_each)
        for scenario in feature.scenarios:
            self.prepare_scenario(scenario)
        if feature.exception is not None:
            self.prepare_exception(feature.exception)
        self.indentation_level -= 4

        self.__push_to_display(self.prepare_border(color, 150))

    def prepare_scenario(self, scenario):
        if not scenario.ran:
            color = self.grey
        elif scenario.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(color(f'Scenario: {scenario.description}'))
        self.indentation_level += 4
        for given in scenario.given:
            self.prepare_given(given)
        for when in scenario.when:
            self.prepare_when(when)
        for then in scenario.then:
            self.prepare_then(then)
        if scenario.exception is not None:
            self.prepare_exception(scenario.exception)
        self.indentation_level -= 4

    def prepare_before_each(self, before_each):
        if not before_each.ran:
            color = self.grey
        elif before_each.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(
            color(f"BeforeEach: {before_each.function.__name__} {before_each.kwargs if before_each.kwargs else ''}")
        )

    def prepare_given(self, given):
        if not given.ran:
            color = self.grey
        elif given.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(color(f"Given: {given.given_function.__name__} {given.kwargs if given.kwargs else ''}"))

    def prepare_when(self, when):
        if not when.ran:
            color = self.grey
        elif when.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(color(f"When: {when.when_function.__name__} {when.kwargs if when.kwargs else ''}"))

    def prepare_then(self, then):
        if not then.ran:
            color = self.grey
        elif then.passed:
            color = self.cyan
        else:
            color = self.red

        self.__push_to_display(color(f"Then: {then.then_function.__name__} {then.kwargs if then.kwargs else ''}"))

    def prepare_exception(self, exception):
        if str(exception):
            exception_string = f'{str(exception)}\n'
        else:
            exception_string = f'{exception.__class__.__name__}\n'

        traceback_string = f'{extract_traceback(exception)}'

        self.__push_to_display(self.yellow((exception_string + traceback_string).rstrip()))

    def prepare_border(self, color, length):
        return color('=' * length)

    def prepare_statistics(self, suite):
        color = self.cyan if suite.passed else self.red

        self.__push_to_display(
            color(
                f'{suite.num_features_passed} Features passed, {suite.num_features_failed} failed.\n'
                f'{suite.num_scenarios_passed} Scenarios passed, {suite.num_scenarios_failed} failed'
            )
        )