import { Page } from "@playwright/test";
import { credentials } from "config/env";
import { ICredentials } from "data/types/credentials.types";
import { HomePage } from "ui/pages/home.page";
import { LoginPage } from "ui/pages/login/login.page";
import { logStep } from "utils/report/logStep.utils.js";

export class LoginUIService {
  homePage: HomePage;
  loginPage: LoginPage;

  constructor(private page: Page) {
    this.homePage = new HomePage(page);
    this.loginPage = new LoginPage(page);
  }

  @logStep("LOGIN AS ADMIN")
  async loginAsAdmin() {
    return await this.login(credentials);
  }

  @logStep("LOGIN WITH CREDENTIALS UI")
  async login(credentials: ICredentials) {
    await this.loginPage.open();
    await this.loginPage.fillCredentials(credentials);
    await this.loginPage.loginButtonClick();
    await this.homePage.waitForOpened();
    const token = (await this.page.context().cookies()).find((c) => c.name === "Authorization")!.value;
    return token;
  }
}
