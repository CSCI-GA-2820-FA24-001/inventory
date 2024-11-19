Feature: The inventory service back-end
    As a Pet Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my inventory

Background:
    Given the following inventory
        | name        | quantity | condition | stock_level  |
        | CocaCola    | 0        | NEW       | OUT_OF_STOCK |
        | Water       | 5        | NEW       | LOW_STOCK    | 
        | Monster     | 10       | NEW       | IN_STOCK     | 
        | iPad        | 15       | USED       | IN_STOCK     | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all pets
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "CocaCola" in the results
    And I should see "Water" in the results
    And I should see "Monster" in the results
    And I should see "iPad" in the results
    And I should not see "Pepsi" in the results
