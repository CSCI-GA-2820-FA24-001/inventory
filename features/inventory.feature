Feature: The inventory service back-end
    As a Store Owner
    I need a RESTful Inventory service
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

Scenario: List all Inventory
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "CocaCola" in the results
    And I should see "Water" in the results
    And I should see "Monster" in the results
    And I should see "iPad" in the results
    And I should not see "Pepsi" in the results

Scenario: Read an Inventory
    When I visit the "Home Page"
    And I set the "Name" to "Water"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Water" in the results
    And I should not see "CocaCola" in the results
    And I should not see "Monster" in the results
    And I should not see "iPad" in the results
    And I should not see "Pepsi" in the results

Scenario: Search for Condition "NEW"
    When I visit the "Home Page"
    And I select "NEW" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "CocaCola" in the results
    And I should see "Water" in the results
    And I should see "Monster" in the results
    And I should not see "iPad" in the results

Scenario: Search for Stock Level "LOW_STOCK"
    When I visit the "Home Page"
    And I select "LOW_STOCK" in the "Stock Level" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Water" in the results
    And I should not see "CocaCola" in the results
    And I should not see "Monster" in the results
    And I should not see "iPad" in the results

Scenario: Restock an Inventory item by a positive amount
    When I visit the "Home Page"
    And I set the "Name" to "Monster"
    And I press the "Search" button
    And I set the "Restock" to "5"
    And I press the "Restock" button
    Then I should see the message "Success"
    And I should see "15" in the "Quantity" field

Scenario: Restock an Inventory item by a negative amount
    When I visit the "Home Page"
    And I set the "Name" to "iPad"
    And I press the "Search" button
    And I set the "Restock" to "-5"
    And I press the "Restock" button
    Then I should see the message "Success"
    And I should see "10" in the "Quantity" field

Scenario: Update Inventory
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "CocaCola" in the "Name" field
    And I should see "0" in the "Quantity" field
    And I should see "NEW" in the "Condition" field
    And I should see "OUT_OF_STOCK" in the "Stock Level" field
    When I copy the "ID" field 
    And I change "Name" to "Coke"
    And I change "Quantity" to "20"
    And I select "OPENBOX" in the "Condition" dropdown
    And I select "IN_STOCK" in the "Stock Level" dropdown
    And I press the "Update" button
    Then I should see the message "Success"
    When I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Coke" in the "Name" field
    And I should see "20" in the "Quantity" field
    And I should see "OPENBOX" in the "Condition" field
    And I should see "IN_STOCK" in the "Stock Level" field

Scenario: Delete Inventory
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "CocaCola" in the "Name" field
    And I should see "0" in the "Quantity" field
    And I should see "NEW" in the "Condition" field
    And I should see "OUT_OF_STOCK" in the "Stock Level" field
    When I copy the "ID" field
    And I press the "Delete" button
    Then I should see the message "Inventory has been Deleted!"
    When I press the "Search" button
    Then I should not see "CocaCola" in the results