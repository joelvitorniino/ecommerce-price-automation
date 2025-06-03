import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { ToastContext } from '../../App';
import './Toast.css';

interface ToastProps {
  message: string;
  visible: boolean;
}

const Toast: React.FC<ToastProps> = ({ message, visible }) => {
  const { showToast } = useContext(ToastContext);

  if (!visible) return null;

  return (
    <div className="toast">
      <span className="toast-icon">🛒</span>
      <span>{message}</span>
      <Link to="/cart" className="toast-link" onClick={() => showToast('')}>
        View Cart
      </Link>
    </div>
  );
};

export default Toast;