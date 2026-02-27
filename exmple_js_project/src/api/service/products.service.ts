import { ProductsApi } from "api/api/products.api";
import { generateProductData } from "data/salesPortal/products/generateProductData";
import { createProductSchema } from "data/schemas/products/create.schema";
import { STATUS_CODES } from "data/statusCodes";
import { IProduct, IProductFromResponse } from "data/types/product.types";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { logStep } from "utils/report/logStep.utils.js";

export const getFieldValues = <T, K extends keyof T>(entities: T[], field: K): Array<T[K]> =>
  entities.map((entity) => entity[field]);

export class ProductsApiService {
  constructor(private productsApi: ProductsApi) {}

  @logStep("CREATE PRODUCT - API")
  async create(token: string, productData?: IProduct): Promise<IProductFromResponse> {
    const data = generateProductData(productData);
    const response = await this.productsApi.create(data, token);
    validateResponse(response, {
      status: STATUS_CODES.CREATED,
      IsSuccess: true,
      ErrorMessage: null,
      schema: createProductSchema,
    });
    return response.body.Product;
  }

  @logStep("UPDATE PRODUCT - API")
  async update(token: string, id: string, newProductData: IProduct): Promise<IProductFromResponse> {
    const data = generateProductData(newProductData);
    const response = await this.productsApi.update(id, data, token);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: createProductSchema,
    });
    return response.body.Product;
  }

  @logStep("DELETE PRODUCT - API")
  async delete(token: string, id: string) {
    const response = await this.productsApi.delete(id, token);
    validateResponse(response, {
      status: STATUS_CODES.DELETED,
    });
  }

  @logStep("DELETE MULTIPLE PRODUCTS - API")
  async deleteProducts(token: string, ids: string[]) {
    for (const id of ids) {
      await this.delete(token, id);
    }
  }

  @logStep("DELETE ALL PRODUCTS - API")
  async deleteAllProducts(token: string) {
    const productsResponse = await this.productsApi.getAll(token);
    validateResponse(productsResponse, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });
    const products = productsResponse.body.Products;
    const ids = products.map((product) => product._id);
    await this.deleteProducts(token, ids);
  }

  @logStep("BULK CREATE PRODUCTS - API")
  public async bulkCreate(token: string, amount: number, customData: Partial<IProduct>[] = []) {
    return await Promise.all(
      Array.from({ length: amount }, (_, idx) => this.create(token, generateProductData(customData[idx]))),
    );
  }
}
