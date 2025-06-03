import { useContext } from 'react';
import { ToastContext } from '../../App';
import type { Product } from '../../types';
import './ProductCard.css';

interface ProductCardProps {
  product: Product;
  onAddToCart: () => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
  const { showToast } = useContext(ToastContext);

  const handleAddToCart = () => {
    onAddToCart();
    showToast(`${product.name} added to cart`);
  };

  return (
    <div className="product-card">
      <div className="product-image-container">
        <img src={product.image} alt={product.name} className="product-image" />
      </div>
      <div className="product-details">
        <h3>{product.name}</h3>
        <p className="description">{product.description}</p>
        <p className="price">R$ {product.currentPrice.toFixed(2)}</p>
        <button onClick={handleAddToCart}>Add to Cart</button>
      </div>
    </div>
  );
};

export default ProductCard;