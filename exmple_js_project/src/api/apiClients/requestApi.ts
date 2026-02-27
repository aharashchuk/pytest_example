import { APIRequestContext, APIResponse, test, TestStepInfo } from "@playwright/test";
import { IRequestOptions, IResponse } from "data/types/core.types";
import { BaseApiClient } from "./baseApiClient";
import _ from "lodash";
import { maskSecrets } from "../../utils/maskSecrets";

export class RequestApi extends BaseApiClient {
  constructor(private requestContext: APIRequestContext) {
    super();
  }

  private response: APIResponse | undefined;

  async send<T extends object | null>(options: IRequestOptions): Promise<IResponse<T>> {
    return await test.step(`Request ${options.method.toUpperCase()} ${options.url}`, async (step) => {
      try {
        await this.attachRequest(options, step);
        this.response = await this.requestContext.fetch(
          options.baseURL + options.url,
          _.omit(options, ["baseURL", "url"]),
        );
        const result = await this.transformResponse();
        await this.attachResponse(options, result, step);
        return result;
      } catch (err) {
        console.log("Error message: " + (err as Error).message);
        console.log("Cause: " + JSON.stringify((err as Error).cause));
        await step.attach("Error", {
          body: String(err),
          contentType: "text/plain",
        });
        throw err;
      }
    });
  }

  protected async transformResponse() {
    let body;
    const contentType = this.response!.headers()["content-type"] || "";
    if (contentType.includes("application/json")) {
      body = await this.response!.json();
    } else {
      body = await this.response!.text();
    }

    return {
      status: this.response!.status(),
      body,
      headers: this.response!.headers(),
    };
  }

  private async attachRequest(options: IRequestOptions, step: TestStepInfo) {
    const stringData = JSON.stringify(
      {
        headers: options.headers,
        ...(options.data && { body: options.data }),
      },
      null,
      2,
    );

    const maskedData = maskSecrets(stringData);
    await step.attach(`Request ${options.method.toUpperCase()} ${options.url}`, {
      body: maskedData,
      contentType: "application/json",
    });
  }

  private async attachResponse<T extends object | null>(
    options: IRequestOptions,
    response: IResponse<T>,
    step: TestStepInfo,
  ) {
    const stringData = JSON.stringify(
      {
        headers: response.headers,
        body: response.body,
      },
      null,
      2,
    );

    const maskedData = maskSecrets(stringData);
    await step.attach(`Response ${response.status} ${options.method.toUpperCase()} ${options.url}`, {
      body: maskedData,
      contentType: "application/json",
    });
  }
}
