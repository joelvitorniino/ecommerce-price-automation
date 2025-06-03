export interface Product {
  id: string;
  name: string;
  description: string;
  originalPrice: number;
  currentPrice: number;
  image: string;
  category: string;
  lastUpdate: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface PriceHistory {
  price: number;
  timestamp: string;
}

export interface Order {
  id: string;
  items: CartItem[];
  total: number;
  customerInfo: {
    name: string;
    email: string;
    address: string;
  };
  timestamp: string;
}