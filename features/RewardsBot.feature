Feature: RewardsBot Features

    Scenario Outline: User can check their own balance
        Given the rewards bot is running
        And   I type "<command>"
        Then  I should see the rewards bot display my balance stored on the database

  Examples: commands
    | command |
    | $bal    |

    Scenario Outline: User can check other registered users balance
        Given the rewards bot is running
        And   I type "<command> <registeredUser>"
        And   "<registeredUser>" is registered
        Then  I should see the rewards bot display "<registeredUser>" balance that is stored on the database

  Examples: commands
    | command | registeredUser |
    | $bal    | registeredU    |

    Scenario Outline: User is alerted when they attempt to get a balance of a user not registered to the database
        Given the rewards bot is running
        And   I type "$bal <unregisteredUser>"
        And   "<unregisteredUser>" is not registered
        Then  I should see an alert informing the user that "<unregisteredUser>" is not registered to the database

  Examples: commands
    | command | unregisteredUser |
    | $bal    | unregisteredU    |
