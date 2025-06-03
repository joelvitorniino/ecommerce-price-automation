import Cart from '../components/Cart';
import { Link } from 'react-router-dom';
import './css/CartPage.css';

const CartPage: React.FC = () => {
  return (
    <div className="cart-page">
      <Cart />
      <Link to="/checkout" className="checkout-button">Proceed to Checkout</Link>
    </div>
  );
};

export default CartPage;