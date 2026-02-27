import { OrdersApi } from "api/api/orders.api";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { STATUS_CODES } from "data/statusCodes";
import {
  IGetAllOrdersQuery,
  IOrderCreateBody,
  IOrderFromResponse,
  IOrdersResponse,
  IOrderUpdateBody,
} from "data/types/order.types";
import { CustomersApiService } from "api/service/customer.service";
import { ProductsApiService } from "api/service/products.service";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { generateDelivery } from "data/salesPortal/orders/generateDeliveryData";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { EntitiesStore } from "api/service/stores/entities.store";
import { faker } from "@faker-js/faker";
import { logStep } from "utils/report/logStep.utils.js";
import { createOrderSchema } from "data/schemas/orders/create.schema";
import { getAllOrdersSchema } from "data/schemas/orders/getAllOrders.schema";
import { MANAGER_IDS } from "config/env";

export class OrdersApiService {
  constructor(
    private ordersApi: OrdersApi,
    private productsApiService: ProductsApiService,
    private customersApiService: CustomersApiService,
    private entitiesStore: EntitiesStore = new EntitiesStore(),
  ) {}

  trackOrderId(id: string): void {
    this.entitiesStore.trackOrders(id);
  }

  trackCustomerId(id: string): void {
    this.entitiesStore.trackCustomers(id);
  }

  trackProductIds(ids: string[]): void {
    this.entitiesStore.trackProducts(ids);
  }

  @logStep("CREATE ORDER - API")
  async create(token: string, customerId: string, productIds: string[]): Promise<IOrderFromResponse> {
    const payload: IOrderCreateBody = {
      customer: customerId,
      products: productIds,
    };

    const response = await this.ordersApi.create(token, payload);

    validateResponse(response, {
      status: STATUS_CODES.CREATED,
      IsSuccess: true,
      ErrorMessage: null,
      schema: createOrderSchema,
    });

    return response.body.Order;
  }

  @logStep("CREATE ORDER AND ENTITIES - API")
  async createOrderAndEntities(token: string, numberOfProducts: number): Promise<IOrderFromResponse> {
    const customersService = this.customersApiService;
    const productsService = this.productsApiService;

    const createdCustomer = await customersService.create(token);
    this.entitiesStore.trackCustomers(createdCustomer._id);

    const orderData: IOrderCreateBody = {
      customer: createdCustomer._id,
      products: [],
    };

    const createdProductIds: string[] = [];
    for (let i = 0; i < numberOfProducts; i++) {
      const createdProduct = await productsService.create(token);
      createdProductIds.push(createdProduct._id);
      orderData.products.push(createdProduct._id);
    }
    this.entitiesStore.trackProducts(createdProductIds);

    const response = await this.ordersApi.create(token, orderData);
    const order = response.body.Order;
    this.entitiesStore.trackOrders(order._id);
    return order;
  }

  @logStep("CREATE ORDER WITH DELIVERY - API")
  async createOrderWithDelivery(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderAndEntities(token, numberOfProducts);
    const orderWithDelivery = await this.ordersApi.addDelivery(token, createdOrder._id, generateDelivery());
    validateResponse(orderWithDelivery, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return orderWithDelivery.body.Order;
  }

  @logStep("CREATE ORDER IN PROCESS - API")
  async createOrderInProcess(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderWithDelivery(token, numberOfProducts);
    const order = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.PROCESSING, token);
    validateResponse(order, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return order.body.Order;
  }

  @logStep("UPDATE ORDER STATUS - API")
  async updateStatus(token: string, orderId: string, status: ORDER_STATUS) {
    const response = await this.ordersApi.updateStatus(orderId, status, token);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return response.body.Order;
  }

  @logStep("CREATE CANCELED ORDER - API")
  async createCanceledOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderWithDelivery(token, numberOfProducts);
    const order = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.CANCELED, token);
    validateResponse(order, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return order.body.Order;
  }

  @logStep("CREATE ORDER IN SPECIFIC STATUS - API")
  async createOrderInStatus(
    token: string,
    numberOfProducts: number,
    status: ORDER_STATUS,
    managerId?: string,
  ): Promise<IOrderFromResponse> {
    const createdOrder = await this.createOrderWithDelivery(token, numberOfProducts);
    managerId = managerId || MANAGER_IDS[0] || "";
    const assignRes = await this.ordersApi.assingManager(token, createdOrder._id, managerId);
    validateResponse(assignRes, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getOrderSchema,
    });

    switch (status) {
      case ORDER_STATUS.DRAFT:
        return createdOrder;

      case ORDER_STATUS.CANCELED: {
        const canceled = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.CANCELED, token);
        validateResponse(canceled, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        return canceled.body.Order;
      }

      case ORDER_STATUS.PROCESSING: {
        const processing = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.PROCESSING, token);
        validateResponse(processing, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        return processing.body.Order;
      }

      case ORDER_STATUS.PARTIALLY_RECEIVED: {
        if (!createdOrder.products || createdOrder.products.length < 2) {
          throw new Error("Partial receive requires at least two products in the order.");
        }
        // Move to processing first
        const toProcessing = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.PROCESSING, token);
        validateResponse(toProcessing, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        const processingOrder = toProcessing.body.Order;

        const firstProductId = processingOrder.products[0]!._id;
        const partial = await this.ordersApi.receiveProducts(processingOrder._id, [firstProductId], token);
        validateResponse(partial, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        return partial.body.Order;
      }

      case ORDER_STATUS.RECEIVED: {
        if (!createdOrder.products || createdOrder.products.length < 1) {
          throw new Error("Received status requires at least one product in the order.");
        }
        const toProcessing = await this.ordersApi.updateStatus(createdOrder._id, ORDER_STATUS.PROCESSING, token);
        const processingOrder = toProcessing.body.Order;
        const received = await this.ordersApi.receiveProducts(
          processingOrder._id,
          processingOrder.products.map((p) => p._id),
          token,
        );
        validateResponse(received, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        return received.body.Order;
      }

      default: {
        const updated = await this.ordersApi.updateStatus(createdOrder._id, status, token);
        validateResponse(updated, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        return updated.body.Order;
      }
    }
  }

  @logStep("CREATE PARTIALLY RECEIVED ORDER - API")
  async createPartiallyReceivedOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderInProcess(token, numberOfProducts);
    const order = await this.ordersApi.receiveProducts(createdOrder._id, [createdOrder.products[0]!._id], token);
    validateResponse(order, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return order.body.Order;
  }

  @logStep("CREATE RECEIVED ORDER - API")
  async createReceivedOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderInProcess(token, numberOfProducts);
    const order = await this.ordersApi.receiveProducts(
      createdOrder._id,
      createdOrder.products.map((product) => product._id),
      token,
    );
    validateResponse(order, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    return order.body.Order;
  }

  @logStep("DELETE ORDER - API")
  async delete(token: string, id: string) {
    const res = await this.ordersApi.delete(token, id);
    validateResponse(res, { status: STATUS_CODES.DELETED });
  }

  @logStep("UPDATE ORDER - API")
  async update(token: string, id: string, payload: IOrderUpdateBody): Promise<IOrderFromResponse> {
    const res = await this.ordersApi.update(token, id, payload);
    validateResponse(res, { status: STATUS_CODES.OK });
    return res.body.Order;
  }

  @logStep("DELETE ORDER AND ENTITIES - API")
  async deleteOrderAndEntities(token: string, orderId: string): Promise<void> {
    // Backward-compatible cleanup by specific orderId
    const response = await this.ordersApi.getById(orderId, token);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getOrderSchema,
    });
    const order = response.body.Order;
    const customerId = order.customer._id;
    const productIds = order.products.map((product) => product._id);

    // delete order first, then related entities
    await this.delete(token, orderId);
    if (customerId) {
      await this.customersApiService.delete(token, customerId);
    }
    if (productIds.length > 0) {
      await this.productsApiService.deleteProducts(token, productIds);
    }

    // keep store in sync to avoid double-deletes later
    this.entitiesStore.trackOrders(orderId);
    this.entitiesStore.trackCustomers(customerId);
    this.entitiesStore.trackProducts(productIds);
  }

  // New: full cleanup by using only token (for after hooks)
  @logStep("FULL DELETE ORDERS AND ENTITIES - API")
  async fullDelete(token: string): Promise<void> {
    const orders = this.entitiesStore.getOrderIds();
    const customers = this.entitiesStore.getCustomerIds();
    const products = this.entitiesStore.getProductIds();

    await Promise.all(orders.map((orderId) => this.delete(token, orderId)));
    await Promise.all(customers.map((customerId) => this.customersApiService.delete(token, customerId)));
    await Promise.all(products.map((productId) => this.productsApiService.delete(token, productId)));

    this.entitiesStore.clear();
  }

  @logStep("ADD COMMENT - API")
  async addComment(token: string, orderId: string, text?: string) {
    const response = await this.ordersApi.addComment(token, orderId, text || faker.lorem.sentence(5));
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getOrderSchema,
    });
    return response.body.Order.comments[response.body.Order.comments.length - 1];
  }

  @logStep("DELETE COMMENT - API")
  async deleteComment(token: string, orderId: string, commentId: string) {
    const response = await this.ordersApi.deleteComment(token, orderId, commentId);
    validateResponse(response, {
      status: STATUS_CODES.DELETED,
    });
    return response;
  }

  @logStep("CREATE CUSTOMER AND PRODUCTS - API")
  async createCustomerAndProducts(
    token: string,
    productsCount: number,
  ): Promise<{
    customerId: string;
    customerName: string;
    productIds: string[];
    productNames: string[];
  }> {
    const customer = await this.customersApiService.create(token);
    this.entitiesStore.trackCustomers(customer._id);

    const productIds: string[] = [];
    const productNames: string[] = [];
    for (let i = 0; i < productsCount; i++) {
      const product = await this.productsApiService.create(token);
      productIds.push(product._id);
      productNames.push(product.name);
    }
    this.entitiesStore.trackProducts(productIds);

    return { customerId: customer._id, productIds, customerName: customer.name, productNames };
  }

  @logStep("GET ALL ORDERS - API")
  async getAll(token: string, params: IGetAllOrdersQuery): Promise<IOrdersResponse> {
    const response = await this.ordersApi.getAll(token, params);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getAllOrdersSchema,
    });
    return response.body;
  }

  @logStep("ASSIGN MANAGER TO ORDER - API")
  async assignManager(token: string, orderId: string, managerId: string): Promise<IOrderFromResponse> {
    const response = await this.ordersApi.assingManager(token, orderId, managerId);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getAllOrdersSchema,
    });
    return response.body.Order;
  }

  @logStep("UNASSIGN MANAGER FROM ORDER - API")
  async unassignManager(token: string, orderId: string): Promise<IOrderFromResponse> {
    const response = await this.ordersApi.unassingManager(token, orderId);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getOrderSchema,
    });
    return response.body.Order;
  }

  @logStep("GET AVAILABLE MANAGERS - API")
  async getAvailableManagers(): Promise<string[]> {
    return MANAGER_IDS;
  }
}
