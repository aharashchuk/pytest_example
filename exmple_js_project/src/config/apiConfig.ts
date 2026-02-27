import { SALES_PORTAL_API_URL } from "./env";

export const apiConfig = {
  baseURL: SALES_PORTAL_API_URL,
  endpoints: {
    products: "/api/products",
    productById: (id: string) => `/api/products/${id}/`,
    productsAll: "/api/products/all",
    login: "/api/login",
    metrics: "/api/metrics",
    customers: "/api/customers",
    customerById: (id: string) => `/api/customers/${id}/`,
    customersAll: "/api/customers/all",
    orders: "/api/orders",
    orderById: (id: string) => `/api/orders/${id}/`,
    ordersAll: "/api/orders/all",
    orderDelivery: (id: string) => `/api/orders/${id}/delivery`,
    orderReceive: (id: string) => `/api/orders/${id}/receive`,
    orderStatus: (id: string) => `/api/orders/${id}/status`,
    orderAssignManager: (orderId?: string, managerId?: string) => `/api/orders/${orderId}/assign-manager/${managerId}`, // data > types > user.types.ts
    orderUnassignManager: (orderId?: string) => `/api/orders/${orderId}/unassign-manager`, // data > types > user.types.ts
    orderComments: (orderId: string) => `/api/orders/${orderId}/comments`,
    orderCommentById: (orderId: string, commentId: string) => `/api/orders/${orderId}/comments/${commentId}`,
    notifications: "/api/notifications",
    notificationAsRead: (id: string) => `/api/notifications/${id}/read`,
    notificationsAllAsRead: "/api/notifications/mark-all-read",
    users: "/api/users",
    userById: (id: string) => `/api/users/${id}/`,
  },
};
