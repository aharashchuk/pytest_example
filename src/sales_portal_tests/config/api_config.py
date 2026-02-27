"""Centralised API endpoint configuration.

All endpoints are expressed as module-level constants (static paths) or
plain functions (parameterised paths) — no class with static methods.

Usage:
    from sales_portal_tests.config import api_config

    url = api_config.LOGIN
    url = api_config.product_by_id("abc123")
"""

from sales_portal_tests.config.env import SALES_PORTAL_API_URL

BASE_URL: str = SALES_PORTAL_API_URL

# ---------------------------------------------------------------------------
# Static endpoints (module constants)
# ---------------------------------------------------------------------------

LOGIN: str = f"{BASE_URL}/api/login"

PRODUCTS: str = f"{BASE_URL}/api/products"
PRODUCTS_ALL: str = f"{BASE_URL}/api/products/all"

CUSTOMERS: str = f"{BASE_URL}/api/customers"
CUSTOMERS_ALL: str = f"{BASE_URL}/api/customers/all"

ORDERS: str = f"{BASE_URL}/api/orders"
ORDERS_ALL: str = f"{BASE_URL}/api/orders/all"

NOTIFICATIONS: str = f"{BASE_URL}/api/notifications"
NOTIFICATIONS_MARK_ALL_READ: str = f"{BASE_URL}/api/notifications/mark-all-read"

METRICS: str = f"{BASE_URL}/api/metrics"
USERS: str = f"{BASE_URL}/api/users"


# ---------------------------------------------------------------------------
# Parameterised endpoints (plain functions)
# ---------------------------------------------------------------------------


def product_by_id(product_id: str) -> str:
    return f"{PRODUCTS}/{product_id}/"


def customer_by_id(customer_id: str) -> str:
    return f"{CUSTOMERS}/{customer_id}/"


def order_by_id(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/"


def order_delivery(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/delivery"


def order_status(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/status"


def order_receive(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/receive"


def order_assign_manager(order_id: str, manager_id: str) -> str:
    return f"{ORDERS}/{order_id}/assign-manager/{manager_id}"


def order_unassign_manager(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/unassign-manager"


def order_comments(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/comments"


def order_comment_by_id(order_id: str, comment_id: str) -> str:
    return f"{ORDERS}/{order_id}/comments/{comment_id}"


def notification_as_read(notification_id: str) -> str:
    return f"{NOTIFICATIONS}/{notification_id}/read"


def user_by_id(user_id: str) -> str:
    return f"{USERS}/{user_id}/"
