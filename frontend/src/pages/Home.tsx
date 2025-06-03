import { useEffect } from 'react';
import { toast } from 'react-toastify';
import { useProducts } from '../hooks/useProducts';
import { usePriceUpdates } from '../hooks/usePriceUpdates';
import ProductList from '../components/ProductList';
import PriceMonitor from '../components/PriceMonitor';
import './css/Home.css';

const Home: React.FC = () => {
  const { products, loading: initialLoading, error, refetch } = useProducts();
  const { products: updatedProducts, isConnected, loading: priceLoading } = usePriceUpdates(products);

  useEffect(() => {
    if (initialLoading) {
      const toastId = toast.loading('Loading products...', {
        position: 'bottom-center',
        theme: 'light',
        className: 'custom-toast',
      });
      return () => {
        toast.dismiss(toastId);
      };
    } else if (error) {
      toast.error(error, {
        position: 'bottom-center',
        theme: 'light',
        className: 'custom-toast',
      });
    }
  }, [initialLoading, error]);

  if (error) return (
    <div className="error">
      <p>{error}</p>
      <button onClick={refetch}>Retry</button>
    </div>
  );

  return (
    <div className="home-container">
      <PriceMonitor />
      <div className="connection-status">
        <span className={`status-indicator ${isConnected ? 'online' : 'offline'}`}></span>
        <span>{isConnected ? 'Connected to server' : 'Disconnected - showing cached data'}</span>
      </div>
      {priceLoading && (
        <div className="price-loading-overlay">
          <div className="price-loading">
            <div className="spinner"></div>
            <span>Updating prices...</span>
          </div>
        </div>
      )}
      <ProductList products={updatedProducts} />
    </div>
  );
};

export default Home;