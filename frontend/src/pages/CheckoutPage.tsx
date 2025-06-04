import React, { Suspense, lazy } from 'react';

// Lazy load do Checkout
const Checkout = lazy(() => import('../components/Checkout'));

const CheckoutPage: React.FC = () => {
  return (
    <Suspense fallback={<div>Loading checkout...</div>}>
      <Checkout />
    </Suspense>
  );
};

export default CheckoutPage;
