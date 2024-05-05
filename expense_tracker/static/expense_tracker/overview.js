// Create a new element (e.g., a paragraph)
let newElement = document.createElement("p");

// Set the content of the new element to the value of your variable
newElement.textContent = myVariable;

// Find the container where you want to add the new element
let container = document.getElementById("content-container");

// Append the new element to the container
container.appendChild(newElement);
