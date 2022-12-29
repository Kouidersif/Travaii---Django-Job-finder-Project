console.log('hello admin');


var stripe = Stripe('pk_live_51Lz03SKORmC2RvgXf0IAm5tseSPsDozduvh8jFgRwCdn4fxeMKZAAPL6JC7btx654sLBbJBhvvhKo6o7Xc0NYWHB00Xm3uEJE0');

var checkoutButton = document.getElementById('checkout-button');

checkoutButton.addEventListener('click', function() {
  stripe.redirectToCheckout({
    // Make the id field from the Checkout Session creation API response
    // available to this file, so you can provide it as argument here
    // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
    sessionId: sessionid
  }).then(function (result) {
    // If `redirectToCheckout` fails due to a browser or network
    // error, display the localized error message to your customer
    // using `result.error.message`.
  });
});