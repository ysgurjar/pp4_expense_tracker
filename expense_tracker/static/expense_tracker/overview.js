// Load the Visualization API and the piechart package.
google.charts.load('current', {
    'packages': ['corechart']
});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table, 
// instantiates the pie chart, passes in the data and
// draws it.
document.addEventListener("DOMContentLoaded", () => {
    // Check for the presence of the container and chart divs
    var container = document.getElementById("data-container");
    var chartDiv = document.getElementById("chart_div");

    if (container && chartDiv) {
        // Extracting the data attribute
        var trial = container.getAttribute("data-trial");
        
        // Step 1: Define a JavaScript variable
        var my_variable = "Hello from JavaScript!";

        // Step 2: Create a new `div` element
        var newDiv = document.createElement("div");

        // Step 3: Create a new `p` tag
        var p = document.createElement("p");

        // Step 4: Set the text content of the `p` tag to the variable value
        p.textContent = my_variable;

        // Step 5: Append the `p` tag inside the new `div`
        newDiv.appendChild(p);

        // Step 6: Append the new `div` to the document body or container
        document.body.appendChild(newDiv);

        // Now draw the chart since both divs are present
        drawChart();
    } else {
        // Retry if the required elements aren't present yet
        setTimeout(() => document.dispatchEvent(new Event("DOMContentLoaded")), 100);
    }
});

function drawChart() {
    var chartDiv = document.getElementById('chart_div');
    if (chartDiv) {
        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Topping');
        data.addColumn('number', 'Slices');
        data.addRows([
            ['Mushrooms', 3],
            ['Onions', 1],
            ['Olives', 1],
            ['Zucchini', 1],
            ['Pepperoni', 2]
        ]);

        // Set chart options
        var options = {
            'title': 'How Much Pizza I Ate Last Night',
            'width': 400,
            'height': 300
        };

        // Instantiate and draw the chart, passing in some options.
        var chart = new google.visualization.PieChart(chartDiv);
        chart.draw(data, options);
    }
}