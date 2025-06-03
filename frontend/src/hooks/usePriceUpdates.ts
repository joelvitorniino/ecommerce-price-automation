import { useState, useEffect } from 'react';
import type { Product } from '../types';
import { fetchProducts } from '../services/api';

export const usePriceUpdates = (initialProducts: Product[]) => {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [isConnected, setIsConnected] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const pollPrices = async () => {
      console.log('Price update started:', new Date().toISOString());
      setLoading(true);
      try {
        const startTime = Date.now();
        const updatedProducts = await fetchProducts();
        setProducts(updatedProducts);
        setIsConnected(true);
        // Ensure minimum loading duration of 1 second
        const elapsed = Date.now() - startTime;
        const remaining = 1000 - elapsed;
        if (remaining > 0) {
          await new Promise((resolve) => setTimeout(resolve, remaining));
        }
      } catch (error) {
        console.error('Price update failed:', error);
        setIsConnected(false);
      } finally {
        setLoading(false);
        console.log('Price update completed:', new Date().toISOString());
      }
    };

    const interval = setInterval(pollPrices, 5000);

    return () => clearInterval(interval);
  }, []);

  return { products, isConnected, loading };
};