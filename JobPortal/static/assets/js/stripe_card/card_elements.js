// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = Stripe('pk_test_51Lz03SKORmC2RvgXRhtthq6yKQVLC1xLCCSq7PWqJ8HqFClSjSOtvQBDN7ImsLdRilbvCTbe1XBQE7ppeKP3D5tL007zG2iI6B');


const options = {
    clientSecret: '{{client_secret}}',
    // Fully customizable with appearance API.
    appearance: {/*...*/},
  };
  
  // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
  const elements = stripe.elements(options);
  
  // Create and mount the Payment Element
  const paymentElement = elements.create('payment');
  paymentElement.mount('#payment-element');