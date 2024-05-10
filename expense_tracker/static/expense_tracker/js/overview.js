/* jshint esversion: 11 */
/* global Chart */
// Access the JSON data stored by Django in the HTML
const rawData = document.getElementById('totals').textContent;

// Need to parse twice to be able to get correct value
const myData = JSON.parse(JSON.parse(rawData));
const total_income = parseInt(myData.total_income);  // Parse the income to integer
const total_expense = parseInt(myData.total_expense);  // Parse the expense to integer

// bar chart for total income and expense
const ctx = document.getElementById('mychart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Total Income', 'Total Expense'],
        datasets: [{
            label: 'Financial Overview',
            data: [total_income, total_expense],  
            backgroundColor: [
                'rgba(54, 162, 235, 0.8)',  // Color for Total Income
                'rgba(255, 99, 132, 0.8)'   // Color for Total Expense
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
