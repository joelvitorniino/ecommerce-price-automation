import React, { useEffect, Suspense, lazy } from 'react';
import { toast } from 'react-toastify';
import { useProducts } from '../hooks/useProducts';
import { usePriceUpdates } from '../hooks/usePriceUpdates';
import './css/Home.css';

// Lazy load dos componentes
const ProductList = lazy(() => import('../components/ProductList'));
const PriceMonitor = lazy(() => import('../components/PriceMonitor'));

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

  if (error && products.length === 0) {
    return (
      <div className="error">
        <p>{error}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return (
    <div className="home-container">
      <Suspense fallback={<div>Loading price monitor...</div>}>
        <PriceMonitor />
      </Suspense>
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
      <Suspense fallback={<div>Loading products...</div>}>
        <ProductList products={updatedProducts} />
      </Suspense>
    </div>
  );
};

export default Home;
