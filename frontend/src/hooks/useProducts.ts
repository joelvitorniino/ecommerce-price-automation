import { useState, useEffect } from 'react';
import type { Product } from '../types';
import { fetchProducts } from '../services/api';

const LOCAL_STORAGE_KEY = 'cached_products';

export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await fetchProducts();
      setProducts(data);
      setError(null);
      localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(data));
    } catch (err) {
      console.error('API fetch failed:', err);
      const cached = localStorage.getItem(LOCAL_STORAGE_KEY);
      if (cached) {
        const parsed: Product[] = JSON.parse(cached);
        setProducts(parsed);
        setError(null); // Limpa o erro porque estamos usando o cache
      } else {
        setError('Failed to load products. Using cached data if available.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const cached = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (cached) {
      const parsed: Product[] = JSON.parse(cached);
      setProducts(parsed);
      setLoading(false);
    }
    fetchData();
  }, []);

  return { products, loading, error, refetch: fetchData };
};
