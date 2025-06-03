import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { CartContext } from '../../App';
import type { Order, CartItem } from '../../types';
import './Checkout.css';

const Checkout: React.FC = () => {
  const { cart, clearCart } = useContext(CartContext);
  const navigate = useNavigate();
  const [customerInfo, setCustomerInfo] = useState({ name: '', email: '', address: '' });

  const total = cart.reduce((sum, item) => sum + item.product.currentPrice * item.quantity, 0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const order: Order = {
      id: Date.now().toString(),
      items: cart,
      total,
      customerInfo,
      timestamp: new Date().toISOString(),
    };
    localStorage.setItem('lastOrder', JSON.stringify(order));
    clearCart();
    navigate('/confirmation');
  };

  return (
    <div className="checkout-container">
      <h2>Checkout</h2>
      <div className="checkout-grid">
        <div className="checkout-form">
          <h3>Billing Details</h3>
          <form onSubmit={handleSubmit}>
            <label>
              Full Name
              <input
                type="text"
                value={customerInfo.name}
                onChange={(e) => setCustomerInfo({ ...customerInfo, name: e.target.value })}
                required
              />
            </label>
            <label>
              Email
              <input
                type="email"
                value={customerInfo.email}
                onChange={(e) => setCustomerInfo({ ...customerInfo, email: e.target.value })}
                required
              />
            </label>
            <label>
              Address
              <input
                type="text"
                value={customerInfo.address}
                onChange={(e) => setCustomerInfo({ ...customerInfo, address: e.target.value })}
                required
              />
            </label>
            <button type="submit">Place Order</button>
          </form>
        </div>
        <div className="order-summary">
          <h3>Order Summary</h3>
          <div className="summary-items">
            {cart.map((item: CartItem) => (
              <div key={item.product.id} className="summary-item">
                <span>{item.product.name} (x{item.quantity})</span>
                <span>R$ {(item.product.currentPrice * item.quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <div className="summary-total">
            <span>Total</span>
            <span>R$ {total.toFixed(2)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;