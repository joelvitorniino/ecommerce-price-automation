import type { Product } from '../types';

export const fetchProducts = async (): Promise<Product[]> => {
  console.log('Fetching products from API at', new Date().toISOString());
  const response = await fetch('http://localhost:8000/products', {
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'If-Modified-Since': '0'
    }
  });
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  const data = await response.json();
  console.log(`Received ${data.length} products`, data.map((p: Product) => ({ id: p.id, currentPrice: p.currentPrice })));
  return data.map((item: Product) => ({
    id: item.id,
    name: item.name,
    description: item.description,
    originalPrice: item.originalPrice,
    currentPrice: item.currentPrice,
    category: item.category,
    image: item.image,
    lastUpdate: item.lastUpdate
  }));
};

export const startAutomation = async (): Promise<void> => {
  const response = await fetch('http://localhost:8000/automation/start', {
    method: 'POST',
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'If-Modified-Since': '0'
    }
  });
  if (!response.ok) {
    throw new Error('Failed to start automation');
  }
};

export const stopAutomation = async (): Promise<void> => {
  const response = await fetch('http://localhost:8000/automation/stop', {
    method: 'POST',
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'If-Modified-Since': '0'
    }
  });
  if (!response.ok) {
    throw new Error('Failed to stop automation');
  }
};

export const getAutomationStatus = async (): Promise<{
  is_running: boolean;
  last_update: string | null;
  update_count: number;
  error_count: number;
  interval: number;
  price_range: { min_factor: number; max_factor: number };
}> => {
  const response = await fetch('http://localhost:8000/automation/status', {
    headers: {
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache',
      'If-Modified-Since': '0'
    }
  });
  if (!response.ok) {
    throw new Error('Failed to get automation status');
  }
  const data = await response.json();
  return {
    is_running: data.is_running,
    last_update: data.last_update,
    update_count: data.update_count,
    error_count: data.error_count,
    interval: data.interval,
    price_range: data.price_range
  };
};
