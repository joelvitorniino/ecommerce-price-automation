import React, { Suspense, lazy } from 'react';
import { Link } from 'react-router-dom';
import './css/CartPage.css';

// Lazy load do Cart
const Cart = lazy(() => import('../components/Cart'));

const CartPage: React.FC = () => {
  return (
    <div className="cart-page">
      <Suspense fallback={<div>Loading cart...</div>}>
        <Cart />
      </Suspense>
      <Link to="/checkout" className="checkout-button">
        Proceed to Checkout
      </Link>
    </div>
  );
};

export default CartPage;
