from jasper import Feature, Scenario, step, Expect
from unittest import TestCase
import asyncio


class TestFeatureArithmetic(TestCase):

    def setUp(self):

        @step
        def an_adding_function(context):
            context.function = lambda a, b: a + b

        @step
        def a_multiplication_function(context):
            context.function = lambda a, b: a * b

        @step
        def we_call_it_with_two_negative_numbers(context):
            context.result = context.function(-5, -5)

        @step
        def we_call_it_with_two_positive_numbers(context):
            context.result = context.function(5, 5)

        @step
        def we_will_get_a_negative_number(context):
            Expect(context.result).to_be.less_than(0)

        @step
        def we_will_get_a_positive_number(context):
            Expect(context.result).to_be.greater_than(0)

        self.adding_two_negative_numbers_scenario = Scenario(
            'Adding two negative numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_negative_numbers(),
            then=we_will_get_a_negative_number()
        )
        self.adding_two_positive_numbers_scenario = Scenario(
            'Adding two positive numbers',
            given=an_adding_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.multiplying_two_negative_numbers_scenario = Scenario(
            'Multiplying two negative numbers',
            given=a_multiplication_function(),
            when=we_call_it_with_two_negative_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.multiplying_two_positive_numbers_scenario = Scenario(
            'Multiplying two positive numbers',
            given=a_multiplication_function(),
            when=we_call_it_with_two_positive_numbers(),
            then=we_will_get_a_positive_number()
        )
        self.feature = Feature(
            'Arithmetic',
            scenarios=[
                self.adding_two_negative_numbers_scenario,
                self.adding_two_positive_numbers_scenario,
                self.multiplying_two_negative_numbers_scenario,
                self.multiplying_two_positive_numbers_scenario
            ]
        )

    def test_run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.feature.run())

        for scenario in self.feature.scenarios:
            self.assertTrue(scenario.ran)
            self.assertIsNone(scenario.exception)
            self.assertTrue(scenario.passed)

        self.assertTrue(self.feature.passed)
        self.assertEqual(len(self.feature.successes), 4)
        self.assertEqual(set(self.feature.successes), {
            self.adding_two_negative_numbers_scenario,
            self.adding_two_positive_numbers_scenario,
            self.multiplying_two_negative_numbers_scenario,
            self.multiplying_two_positive_numbers_scenario
        })
        self.assertEqual(len(self.feature.failures), 0)
        self.assertEqual(set(self.feature.failures), set())
        self.assertEqual(self.feature.num_scenarios_passed, 4)
        self.assertEqual(self.feature.num_scenarios_failed, 0)