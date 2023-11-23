var totalPrice = 0; // Variable to store the total price

        function addToCart(coffeeName, coffeePrice) 
        {
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
            cartItem.addEventListener("click", function() 
            {
                alert("Price: $" + coffeePrice.toFixed(2));
            });
        }


/* Close */
function closeNav() 
{
    document.getElementById("myNav").style.height = "0%";
}
/* Open */
function openNav() 
{
    document.getElementById("myNav").style.height = "100%";
}


document.getElementById("FinalCost").textContent = "Total Cost $" + totalPrice.toFixed(2);