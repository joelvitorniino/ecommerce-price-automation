import { useContext } from 'react';
import { CartContext } from '../../App';
import type { CartItem } from '../../types';
import './Cart.css';

const Cart: React.FC = () => {
  const { cart, updateQuantity, removeFromCart } = useContext(CartContext);

  const total = cart.reduce((sum, item) => sum + item.product.currentPrice * item.quantity, 0);

  return (
    <div className="cart-container">
      <h2>Your Cart</h2>
      {cart.length === 0 ? (
        <p className="empty-cart">Your cart is empty</p>
      ) : (
        <>
          <table className="cart-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Subtotal</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {cart.map((item: CartItem) => (
                <tr key={item.product.id}>
                  <td>{item.product.name}</td>
                  <td>R$ {item.product.currentPrice.toFixed(2)}</td>
                  <td>
                    <input
                      type="number"
                      value={item.quantity}
                      min="1"
                      onChange={(e) => updateQuantity(item.product.id, parseInt(e.target.value))}
                      className="quantity-input"
                    />
                  </td>
                  <td>R$ {(item.product.currentPrice * item.quantity).toFixed(2)}</td>
                  <td>
                    <button
                      onClick={() => removeFromCart(item.product.id)}
                      className="remove-button"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="cart-total">
            <h3>Total: R$ {total.toFixed(2)}</h3>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart;