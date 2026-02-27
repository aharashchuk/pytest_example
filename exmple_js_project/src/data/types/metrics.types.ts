import { ITopProducts } from "./product.types";

export interface IOrdersMetrics {
  totalRevenue: number;
  totalOrders: number;
  averageOrderValue: number;
  totalCanceledOrders: number;
  recentOrders: unknown[];
  ordersCountPerDay: unknown[];
}

export interface ICustomersGrowthMetrics {
  date: {
    year: number;
    month: number;
    day: number;
  };
  count: number;
}

export interface ICustomersMetrics {
  totalNewCustomers: number;
  topCustomers: unknown[];
  customerGrowth: ICustomersGrowthMetrics[];
}

export interface IDateMetrics {
  year: number;
  month: number;
  day: number;
}

export interface IProductsMetrics {
  topProducts: ITopProducts[];
}

export interface IResponseMetrics {
  IsSuccess: boolean;
  Metrics: {
    orders: IOrdersMetrics;
    customers: ICustomersMetrics;
    products: IProductsMetrics;
  };
  ErrorMessage: string | null;
}
