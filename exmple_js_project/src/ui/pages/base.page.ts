import { expect, Locator, Page } from "@playwright/test";
import { IResponse } from "data/types/core.types";
import { logStep } from "utils/report/logStep.utils.js";

export abstract class BasePage {
  constructor(protected page: Page) {}

  async interceptRequest<T extends unknown[]>(url: string, triggerAction: (...args: T) => Promise<void>, ...args: T) {
    const [request] = await Promise.all([
      this.page.waitForRequest((request) => request.url().includes(url)),
      triggerAction(...args),
    ]);
    return request;
  }

  async expectRequest<T extends unknown[]>(
    method: string,
    url: string,
    queryParams: Record<string, string>,
    triggerAction: (...args: T) => Promise<void>,
    ...args: T
  ) {
    const [request] = await Promise.all([
      this.page.waitForRequest((request) => {
        const urlAndMethodMatch = request.url().includes(url) && request.method() === method;
        let queryParamMatch = true;
        for (const [paramName, paramValue] of Object.entries(queryParams)) {
          queryParamMatch = request.url().includes(`${paramName}=${paramValue}`);
        }
        return urlAndMethodMatch && queryParamMatch;
      }),
      triggerAction(...args),
    ]);
    expect(request).toBeTruthy();
  }

  async interceptResponse<U extends object | null, T extends unknown[]>(
    url: string,
    triggerAction: (...args: T) => Promise<void>,
    ...args: T
  ): Promise<IResponse<U>> {
    const [response] = await Promise.all([
      this.page.waitForResponse((response) => response.url().includes(url)),
      triggerAction(...args),
    ]);
    return {
      status: response.status(),
      headers: response.headers(),
      body: (await response.json()) as U,
    };
  }

  @logStep("GET AUTH TOKEN FROM COOKIES")
  async getAuthToken() {
    const token = (await this.page.context().cookies()).find((c) => c.name === "Authorization")!.value;
    return token;
  }

  @logStep("FIELD IS DISABLED")
  async expectLocked(input: Locator) {
    if (await input.isDisabled()) {
      await expect(input).toBeDisabled();
      return;
    }
    await expect(input).toHaveJSProperty("readOnly", true);
  }

  @logStep("GET COOKIE BY NAME")
  async getCookieByName(cookieName: string) {
    const cookies = await this.page.context().cookies();
    return cookies.find((c) => c.name === cookieName);
  }
}
