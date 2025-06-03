import { useState, useEffect } from 'react';
import { fetchProducts, getAutomationStatus } from '../services/api';
import type { Product } from '../types';

const CACHE_KEY = 'cachedProducts';

export const usePriceUpdates = (initialProducts: Product[]) => {
  const [products, setProducts] = useState<Product[]>(initialProducts);
  const [isConnected, setIsConnected] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [automationRunning, setAutomationRunning] = useState<boolean>(false);

  // Carrega cache offline ao montar
  useEffect(() => {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed)) {
          setProducts(parsed);
        }
      } catch {
        console.warn('Falha ao carregar cache local');
      }
    }
  }, []);

  // Checa o status da automação
  useEffect(() => {
    const checkAutomationStatus = async () => {
      try {
        const status = await getAutomationStatus();
        setAutomationRunning(status.is_running);
        setIsConnected(true);
      } catch (error) {
        setIsConnected(false);
      }
    };
    checkAutomationStatus();
    const interval = setInterval(checkAutomationStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // Sempre busca os produtos 1x ao montar
  useEffect(() => {
    const fetchInitialProducts = async () => {
      try {
        setLoading(true);
        const updated = await fetchProducts();
        setProducts(updated);
        localStorage.setItem(CACHE_KEY, JSON.stringify(updated));
        setIsConnected(true);
      } catch (error) {
        console.warn('API offline, usando dados em cache');
        setIsConnected(false);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialProducts();
  }, []);

  // Atualiza os preços continuamente apenas se a automação estiver rodando
  useEffect(() => {
    if (!automationRunning) return;

    const updatePrices = async () => {
      try {
        setLoading(true);
        const updated = await fetchProducts();
        setProducts(updated);
        localStorage.setItem(CACHE_KEY, JSON.stringify(updated));
        setIsConnected(true);
      } catch (error) {
        console.warn('API offline, usando dados em cache');
        setIsConnected(false);
      } finally {
        setLoading(false);
      }
    };

    updatePrices();
    const interval = setInterval(updatePrices, 10000);
    return () => clearInterval(interval);
  }, [automationRunning]);

  return { products, isConnected, loading };
};
