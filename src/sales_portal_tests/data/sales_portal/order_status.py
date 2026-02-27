"""Order status and history action enums."""

from enum import StrEnum


class OrderStatus(StrEnum):
    DRAFT = "Draft"
    PROCESSING = "In Process"
    PARTIALLY_RECEIVED = "Partially Received"
    RECEIVED = "Received"
    CANCELED = "Canceled"
    EMPTY = "-"


class OrderHistoryActions(StrEnum):
    CREATED = "Order created"
    CUSTOMER_CHANGED = "Customer changed"
    REQUIRED_PRODUCTS_CHANGED = "Requested products changed"
    PROCESSED = "Order processing started"
    DELIVERY_SCHEDULED = "Delivery Scheduled"
    DELIVERY_EDITED = "Delivery Edited"
    RECEIVED = "Received"
    RECEIVED_ALL = "All products received"
    CANCELED = "Order canceled"
    MANAGER_ASSIGNED = "Manager Assigned"
    MANAGER_UNASSIGNED = "Manager Unassigned"
    REOPENED = "Order reopened"
