$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res.id);
        $("#inventory_name").val(res.name);
        $("#inventory_stock_level").val(res.stock_level);
        $("#inventory_quantity").val(res.quantity);
        $("#inventory_condition").val(res.condition);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_name").val("");
        $("#inventory_stock_level").val("");
        $("#inventory_quantity").val("");
        $("#inventory_condition").val("");
        $("#inventory_restock").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Inventory
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#inventory_name").val();
        let stock_level = $("#inventory_stock_level").val();
        let quantity = $("#inventory_quantity").val();
        let condition = $("#inventory_condition").val();

        let data = {
            "name": name,
            "stock_level": stock_level,
            "quantity": quantity,
            "condition": condition
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/inventory",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an Inventory
    // ****************************************

    $("#update-btn").click(function () {

        let inventory_id = $("#inventory_id").val();
        let name = $("#inventory_name").val();
        let stock_level = $("#inventory_stock_level").val();
        let available = $("#inventory_available").val() == "true";
        let quantity = $("#inventory_quantity").val();
        let condition = $("#inventory_condition").val();

        let data = {
            "name": name,
            "stock_level": stock_level,
            "available": available,
            "quantity": quantity,
            "condition": condition
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/inventory/${inventory_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an Inventory
    // ****************************************

    $("#retrieve-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/inventory/${inventory_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Inventory
    // ****************************************

    $("#delete-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/inventory/${inventory_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Inventory has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inventory_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Inventory
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#inventory_name").val();
        let stock_level = $("#inventory_stock_level").val();
        let quantity = $("#inventory_quantity").val();
        let condition = $("#inventory_condition").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (stock_level) {
            if (queryString.length > 0) {
                queryString += '&stock_level=' + stock_level
            } else {
                queryString += 'stock_level=' + stock_level
            }
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&quantity=' + quantity
            } else {
                queryString += 'quantity=' + quantity
            }
        }
        if (condition) {
            if (queryString.length > 0) {
                queryString += '&condition=' + condition
            } else {
                queryString += 'condition=' + condition
            }
        }
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/inventory?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Stock Level</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Condition</th>'
            table += '</tr></thead><tbody>'
            let firstInventory = "";
            for(let i = 0; i < res.length; i++) {
                let inventory = res[i];
                table +=  `<tr id="row_${i}"><td>${inventory.id}</td><td>${inventory.name}</td><td>${inventory.stock_level}</td><td>${inventory.quantity}</td><td>${inventory.condition}</td></tr>`;
                if (i == 0) {
                    firstInventory = inventory;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstInventory != "") {
                update_form_data(firstInventory)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Restock for a Inventory
    // ****************************************
    $("#restock-btn").click(function () {

        let inventory_id = $("#inventory_id").val();
        let restock_amount = $("#inventory_restock").val();
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/inventory/${inventory_id}/restock/${restock_amount}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
