import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import type { Order } from '../../types';
import './Confirmation.css';

const Confirmation: React.FC = () => {
  const [order, setOrder] = useState<Order | null>(null);

  useEffect(() => {
    const savedOrder = localStorage.getItem('lastOrder');
    if (savedOrder) {
      setOrder(JSON.parse(savedOrder));
    }
  }, []);

  if (!order) return <div className="confirmation-container">No order found.</div>;

  return (
    <div className="confirmation-container">
      <h2>Order Confirmed!</h2>
      <div className="order-details">
        <h3>Order #{order.id}</h3>
        <p><strong>Customer:</strong> {order.customerInfo.name}</p>
        <p><strong>Email:</strong> {order.customerInfo.email}</p>
        <p><strong>Address:</strong> {order.customerInfo.address}</p>
        <p><strong>Order Date:</strong> {new Date(order.timestamp).toLocaleString()}</p>
        <h4>Items</h4>
        <table className="order-items">
          <thead>
            <tr>
              <th>Product</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item) => (
              <tr key={item.product.id}>
                <td>{item.product.name}</td>
                <td>{item.quantity}</td>
                <td>R$ {item.product.currentPrice.toFixed(2)}</td>
                <td>R$ {(item.product.currentPrice * item.quantity).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="order-total">
          <span>Total</span>
          <span>R$ {order.total.toFixed(2)}</span>
        </div>
      </div>
      <Link to="/" className="continue-shopping">Continue Shopping</Link>
    </div>
  );
};

export default Confirmation;