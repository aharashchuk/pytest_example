import { IOrderCreateBody } from "data/types/order.types";
import { OrdersApi } from "api/api/orders.api";
import { CustomersApiService } from "api/service/customer.service";
import { ProductsApiService } from "api/service/products.service";
import { generateDelivery } from "data/salesPortal/orders/generateDeliveryData";
import { ORDER_STATUS } from "data/salesPortal/order-status";

export class OrdersFacadeService {
  constructor(
    private ordersApi: OrdersApi,
    private customerApiService: CustomersApiService,
    private productsApiService: ProductsApiService,
  ) {}

  async create(token: string, numberOfProducts: number) {
    const createdCustomer = await this.customerApiService.create(token);
    const orderData: IOrderCreateBody = {
      customer: createdCustomer._id,
      products: [],
    };
    for (let i = 0; i < numberOfProducts; i++) {
      const createdProduct = await this.productsApiService.create(token);
      orderData.products.push(createdProduct._id);
    }
    const order = await this.ordersApi.create(token, orderData);
    return order;
  }

  async createOrderWithDelivery(token: string, numberOfProducts: number) {
    const createdOrder = await this.create(token, numberOfProducts);
    const orderWithDelivery = await this.ordersApi.addDelivery(token, createdOrder.body.Order._id, generateDelivery());
    return orderWithDelivery;
  }

  async createOrderInProcess(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderWithDelivery(token, numberOfProducts);
    const order = await this.ordersApi.updateStatus(createdOrder.body.Order._id, ORDER_STATUS.PROCESSING, token);
    return order;
  }

  async createCanceledOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderWithDelivery(token, numberOfProducts);
    const order = await this.ordersApi.updateStatus(createdOrder.body.Order._id, ORDER_STATUS.CANCELED, token);
    return order;
  }

  async createPartiallyReceivedOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderInProcess(token, numberOfProducts);
    const order = await this.ordersApi.receiveProducts(
      createdOrder.body.Order._id,
      [createdOrder.body.Order.products[0]!._id],
      token,
    );
    return order;
  }

  async createReceivedOrder(token: string, numberOfProducts: number) {
    const createdOrder = await this.createOrderInProcess(token, numberOfProducts);
    const order = await this.ordersApi.receiveProducts(
      createdOrder.body.Order._id,
      createdOrder.body.Order.products.map((product) => product._id),
      token,
    );
    return order;
  }
}
