var totalPrice = 0; // Variable to store the total price
var popular = false
 
var coffeePopularSpan = document.createElement("span");
            coffeePopularSpan.textContent = coffePopular;

            if (coffePopular) {
                coffeePopularSpan.textContent = " - Popular";
            } else {
                coffeePopularSpan.textContent = " - Not Popular";
            }

        function addToCart(coffeeName, coffeePrice, coffePopular) {
            // Create a new div element for the cart item
            var cartItem = document.createElement("div");
 
            // Create span elements for coffee name and price
            var coffeeNameSpan = document.createElement("span");
            coffeeNameSpan.textContent = coffeeName;
 
            var coffeePriceSpan = document.createElement("span");
            coffeePriceSpan.textContent = " - $" + coffeePrice.toFixed(2);

            

            // Append the spans to the cart item
            cartItem.appendChild(coffeeNameSpan);
            cartItem.appendChild(coffeePriceSpan);
 
            // Append the cart item to the cart
            document.getElementById("cart").appendChild(cartItem);
 
            // Add the price to the total
            totalPrice += coffeePrice;
 
            // Update the total price in the cart
            document.getElementById("totalPrice").textContent = "Total: $" + totalPrice.toFixed(2);
 
            // Add a click event listener to show the price when clicked
            cartItem.addEventListener("click", function() {
                alert("Price: $" + coffeePrice.toFixed(2));
            });
        }