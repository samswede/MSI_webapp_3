$(document).ready(function() {

    // Initialize dropdowns
    $('#dropdown-1').dropdown();
    $('#dropdown-2').dropdown();
    var $dropdown1 = $('#dropdown-1 .menu');
    var $dropdown2 = $('#dropdown-2 .menu');


    // Initialize the slider 1
    $('#slider-1').slider({
        min: 20,
        max: 100,
        start: 20,
        step: 5,
        onChange: function(value) {
          console.log("Value of slider 1: " + value);  // Log the value when slider value changes
        }
    });
    // Initialize the slider 2
    $('#slider-2').slider({
        min: 20,
        max: 100,
        start: 20,
        step: 5,
        onChange: function(value) {
          console.log("Value of slider 2: " + value);  // Log the value when slider value changes
        }
    });

    // Dropdown 1
    $.getJSON('http://127.0.0.1:8000/diseases', function(diseases) {
        // Loop through each state in the returned data
        $.each(diseases, function(i, disease) {
            // Append a new dropdown item for each state
            $dropdown1.append('<div class="item" data-value="' + disease.value + '">' + disease.name + '</div>');
        });

        // Initialize the dropdown
        $('#dropdown-1').dropdown();
    });

    // Button 2, Find Drug Candidates
    // Updates the Dropdown 2 list
    // Event handlers for buttons
    $('#btn-2').click(function() {
        
        // Log that onChange is being triggered
        console.log('Find Drug Candidates Button triggered');

        var disease_label = $('#dropdown-1').dropdown('get value');

        // Log the name chosen disease from the Dropdown 1
        console.log("Chosen Disease label: " + disease_label);

        // Here you can send the disease_name, drug_name, k1 and k2 to your server and get the response
        // Example:
        $.ajax({
            url: 'http://127.0.0.1:8000/drugs_for_disease',
            type: 'POST',
            data: JSON.stringify({ 
                disease_label: disease_label
            }),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(drug_candidates) {
                // Clear any existing items in the dropdown
                $dropdown2.empty();
                // Loop through each state in the returned data
                $.each(drug_candidates, function(i, drug) {
                    // Append a new dropdown item for each state
                    $dropdown2.append('<div class="item" data-value="' + drug.value + '">' + drug.name + '</div>');
                });

                // Initialize the dropdown
                $('#dropdown-2').dropdown();
            },
            error: function (request, status, error) {
                console.error('Error occurred:', error);
            }

        });
    });

    // Dropdown 2
    // Determining contents of Dropdown 2 is triggered by changes to dropdown 1
    // You need to extract the selected disease value and pass it in the POST request

    $('#dropdown-1').dropdown({
        onChange: function(value, text, $selectedItem) {

            // Log that onChange is being triggered
            console.log('onChange triggered');

            // Log the name when dropdown is selected
            console.log("Value of dropdown 1: " + JSON.stringify(value));

            // The value will contain the selected disease value
            // Send a post request for 
            $.ajax({
                url: 'http://127.0.0.1:8000/drugs_for_disease',
                type: 'POST',
                data: JSON.stringify({ name: value }), 
                contentType: "application/json; charset=utf-8",
                dataType: 'json',
                success: function(drug_candidates) {
                    // Clear any existing items in the dropdown
                    $dropdown2.empty();
                    // Loop through each state in the returned data
                    $.each(drug_candidates, function(i, drug) {
                        // Append a new dropdown item for each state
                        $dropdown2.append('<div class="item" data-value="' + drug.value + '">' + drug.name + '</div>');
                    });

                    // Initialize the dropdown
                    $('#dropdown-2').dropdown();
                },
                error: function (request, status, error) {
                    console.error('Error occurred:', error);
                }
            });
        }
    });


    // Event handlers for buttons
    $('#btn-1').click(function() {
        
        // Log that onChange is being triggered
        console.log('Generate Button triggered');

        var disease_label = $('#dropdown-1').dropdown('get value');
        var drug_label = $('#dropdown-2').dropdown('get value');
        var k1 = $('#slider-1').slider('get value');
        var k2 = $('#slider-2').slider('get value');

        // Log the name when dropdown is selected
        console.log("Chosen Disease label: " + disease_label);
        console.log("Chosen Drug label: " + drug_label);
        console.log("Slider 1 value: " + k1);
        console.log("Slider 2 value: " + k2);

        // Here you can send the disease_name, drug_name, k1 and k2 to your server and get the response
        // Example:
        $.ajax({
            url: 'http://127.0.0.1:8000/graph',
            type: 'POST',
            data: JSON.stringify({ 
                disease_label: disease_label,
                drug_label: drug_label,
                k1: k1,
                k2: k2
            }),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function(response) {
                // Handle the response from your server
                //console.log("Graph Response: ", JSON.stringify(response));;
                graphData = response.MOA_network;

                // Use vis-network to render the graphs
                new vis.Network(MOA_network, graphData, {});
            },
            error: function (request, status, error) {
                console.error('Error occurred:', error);
            }

        });
    });
});
