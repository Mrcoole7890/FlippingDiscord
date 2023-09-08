from behave import *
from behave import given, when, use_step_matcher
import parse

@given('the rewards bot is running')
def step_impl(context):
    raise NotImplementedError("Not Implemented Yet.")

@given('I type {text}')
def step_impl(context, text):
    raise NotImplementedError("Not Implemented Yet.")


@then('I should see the rewards bot display my balance stored on the database')
def step_impl(context):
    raise NotImplementedError("Not Implemented Yet.")

@given('{registeredUser} is registered')
def step_impl(context, registeredUser):
    raise NotImplementedError("Not Implemented Yet.")

@then('I should see the rewards bot display {registeredUser} balance that is stored on the database')
def step_impl(context, registeredUser):
    raise NotImplementedError("Not Implemented Yet.")

@given('{registeredUser} is not registered')
def step_impl(context, registeredUser):
    raise NotImplementedError("Not Implemented Yet.")

@then('I should see an alert informing the user that {unregisteredUser} is not registered to the database')
def step_impl(context, unregisteredUser):
    raise NotImplementedError("Not Implemented Yet.")
