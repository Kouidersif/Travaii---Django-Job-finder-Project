console.log('hello sif');


var stripe = Stripe('pk_test_51Lz03SKORmC2RvgXRhtthq6yKQVLC1xLCCSq7PWqJ8HqFClSjSOtvQBDN7ImsLdRilbvCTbe1XBQE7ppeKP3D5tL007zG2iI6B');

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