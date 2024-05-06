document.addEventListener("DOMContentLoaded", function() {
    // Access the JSON data stored by Django in the HTML
    const rawData = document.getElementById('mydata').textContent;
    const myData = JSON.parse(rawData);

    // Now you can use `myData` in your JavaScript code
    console.log(myData);
});
