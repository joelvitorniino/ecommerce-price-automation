import { useContext } from 'react';
import { CartContext } from '../../App';
import ProductCard from '../ProductCard';
import type { Product } from '../../types';
import './ProductList.css';

interface ProductListProps {
  products: Product[];
}

const ProductList: React.FC<ProductListProps> = ({ products }) => {
  const { addToCart } = useContext(CartContext);

  return (
    <div className="product-list-container">
      <h2>Our Products</h2>
      <div className="product-list">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} onAddToCart={() => addToCart(product)} />
        ))}
      </div>
    </div>
  );
};

export default ProductList;