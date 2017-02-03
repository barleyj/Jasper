from jasper import Feature, Scenario, JasperGiven, JasperWhen, JasperThen, Expect


class Given(JasperGiven):
    @staticmethod
    def an_adding_function(a, b):
        return a + b

    @staticmethod
    def a_multiplication_function(a, b):
        return a * b


class When(JasperWhen):
    def we_call_it_with_two_negative_numbers(self):
        return self.context.function(-5, -5)

    def we_call_it_with_two_positive_numbers(self):
        return self.context.function(5, 5)


class Then(JasperThen):
    def we_will_get_a_negative_number(self):
        Expect(self.context.result).to_be.less_than(0)

    def we_will_get_a_positive_number(self):
        Expect(self.context.result).to_be.greater_than(0)

feature = Feature(
    'Arithmetic',
    Scenario(
        'Adding two negative numbers',
        Given('an_adding_function', with_alias='function'),
        When('we_call_it_with_two_negative_numbers'),
        Then('we_will_get_a_negative_number')
    ),
    Scenario(
        'Adding two positive numbers',
        Given('an_adding_function', with_alias='function'),
        When('we_call_it_with_two_positive_numbers'),
        Then('we_will_get_a_negative_number')
    ),
    Scenario(
        'Multiplying two negative numbers',
        Given('a_multiplication_function', with_alias='function'),
        When('we_call_it_with_two_negative_numbers'),
        Then('we_will_get_a_negative_number')
    ),
    Scenario(
        'Multiplying two positive numbers',
        Given('a_multiplication_function', with_alias='function'),
        When('we_call_it_with_two_positive_numbers'),
        Then('we_will_get_a_positive_number')
    )
)
feature.run()
print(feature)



