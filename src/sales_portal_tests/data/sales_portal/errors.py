"""API response error message constants."""


class ResponseErrors:
    BAD_REQUEST = "Incorrect request body"
    UNAUTHORIZED = "Not authorized"
    INCORRECT_DELIVERY = "Incorrect Delivery"
    INVALID_DATE = "Invalid final date"
    CUSTOMER_MISSING = "Missing customer"
    INVALID_ORDER_STATUS = "Invalid order status"
    ORDER_IS_NOT_PROCESSED = "Can't process order. Please, schedule delivery"
    INVALID_PAYLOAD = "Argument passed in must be a string of 12 bytes or a string of 24 hex characters or an integer"

    @staticmethod
    def product_not_found(product_id: str) -> str:
        return f"Product with id '{product_id}' wasn't found"

    @staticmethod
    def customer_not_found(customer_id: str) -> str:
        return f"Customer with id '{customer_id}' wasn't found"

    @staticmethod
    def conflict(name: str) -> str:
        return f"Product with name '{name}' already exists"

    @staticmethod
    def manager_not_found(manager_id: str) -> str:
        return f"Manager with id '{manager_id}' wasn't found"

    @staticmethod
    def order_not_found(order_id: str) -> str:
        return f"Order with id '{order_id}' wasn't found"

    @staticmethod
    def product_not_requested(product_id: str) -> str:
        return f"Product with Id '{product_id}' is not requested"
