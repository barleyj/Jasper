from jasper import step, Expect, ExpectationException


@step
def the_expect_object_will_use_our_actual_data(context):
    Expect(context.expect.actual_data).to_be(context.actual_data)


@step
def the_expect_objects_negate_attribute_will_be_(context, negate):
    Expect(context.expect.negate).to_be(negate)


@step
def the_expect_objects_operator_attribute_will_be(context, operator):
    Expect(context.expect.operator).to_be(operator)


@step
def the_expectation_should_pass(context):
    Expect(type(context.exception)).not_.to_be(ExpectationException)


@step
def the_expectation_should_fail(context):
    Expect(type(context.exception)).to_be(ExpectationException)
