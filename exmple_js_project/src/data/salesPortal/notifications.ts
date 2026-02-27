export enum NOTIFICATIONS {
  PRODUCT_CREATED = "Product was successfully created",
  PRODUCT_DELETED = "Product was successfully deleted",
  PRODUCT_UPDATED = "Product was successfully updated",
  NO_PRODUCTS_FOUND = "No products found. Please add one before creating an order.",

  CUSTOMER_CREATED = "Customer was successfully created",
  CUSTOMER_DELETED = "Customer was successfully deleted",
  CUSTOMER_UPDATED = "Customer was successfully updated",
  NO_CUSTOMERS_FOUND = "No customers found. Please add one before creating an order.",
  CUSTOMER_UNABLE_TO_UPDATE = "Unable to update customer. Please try again later.",
  CUSTOMER_FAILED_TO_UPDATE = "Failed to update customer. Please try again later.",

  ORDER_PROCESSED = "Order processing was successfully started",
  ORDER_CANCELED = "Order was successfully canceled",
  ORDER_REOPENED = "Order was successfully reopened",
  ORDER_CREATED = "Order was successfully created",
  ORDER_UPDATED = "Order was successfully updated",
  ORDER_NOT_CREATED = "Failed to create an order. Please try again later.",
  ORDER_UNABLE_TO_CREATE = "Unable to create an order. Please try again later.",
}

export enum NOTIFICATIONS_TYPES {
  ASSIGNED = "assigned",
  STATUS_CHANGED = "statusChanged",
  CUSTOMER_CHANGED = "customerChanged",
  PRODUCTS_CHANGED = "productsChanged",
  DELIVERY_UPDATED = "deliveryUpdated",
  PRODUCTS_DELIVERED = "productsDelivered",
  MANAGER_CHANGED = "managerChanged",
  COMMENT_ADDED = "commentAdded",
  COMMENT_DELETED = "commentDeleted",
  NEW_ORDER = "newOrder",
  UNASSIGNED = "unassigned",
}

export type ModalCopy = {
  title: string;
  body: string;
  actionButton: string;
};

export const CANCEL_ORDER_MODAL: ModalCopy = {
  title: "Cancel Order",
  body: "Are you sure you want to cancel the order?",
  actionButton: "Yes, Cancel",
};

export const REOPEN_ORDER_MODAL: ModalCopy = {
  title: "Reopen Order",
  body: "Are you sure you want to reopen the order?",
  actionButton: "Yes, Reopen",
};

export const PROCESS_ORDER_MODAL: ModalCopy = {
  title: "Process Order",
  body: "Are you sure you want to process the order?",
  actionButton: "Yes, Process",
};
