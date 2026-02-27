import { expect, Page } from "@playwright/test";
import { SalesPortalPage } from "../salesPortal.page";
import { logStep } from "utils/report/logStep.utils.js";
import { ConfirmationModal } from "../confirmation.modal";
import {
  OrderDetailsHeader,
  OrderDetailsCustomerDetails,
  OrderDetailsRequestedProducts,
  AssignManagerModal,
} from "./components";
import { CommentsTab } from "./components/delivery/comments.tab.page";
import { TIMEOUT_30_S } from "data/salesPortal/constants";
import { EditProductsModal } from "./editProducts.modal";
import { NavBar } from "../navbar.component";
import { DeliveryTab } from "./components/delivery/delivery.tab.page";
import { OrderHistoryTab } from "./components/delivery/orderHistory.tab.page";
import { ScheduleDeliveryPage } from "./components/delivery/scheduleDelivery.page";
import { EditOrderCustomerModal } from "./components/editCustomer.modal";

/**
 * Order Details PageObject orchestrator.
 * Splits the page into components: Header, Customer Details, Requested Products.
 */
export class OrderDetailsPage extends SalesPortalPage {
  readonly navBar = new NavBar(this.page);
  readonly orderInfoContainer = this.page.locator("#order-info-container");
  readonly tabsContainer = this.page.locator("#order-details-tabs-section");
  readonly processOrderButton = this.page.locator("#process-order");
  readonly cancelOrderButton = this.page.locator("#cancel-order");
  readonly reopenOrderButton = this.page.locator("#reopen-order");
  readonly refreshOrderButton = this.page.locator("#refresh-order");
  readonly statusOrderLabel = this.page.locator(
    "div:nth-child(1) > span.text-primary, div:nth-child(1) > span.text-danger",
  );
  readonly notificationToast = this.page.locator(".toast-body");
  // Be tolerant: different FE builds may render different anchors
  readonly uniqueElement = this.page.locator(
    [
      "#order-info-container",
      "#order-details-tabs",
      "#order-details-tabs-section",
      "#order-status-bar-container",
      "#assigned-manager-container",
      "#customer-section",
      "#products-section",
    ].join(", "),
  );

  // Components
  readonly header: OrderDetailsHeader;
  readonly customerDetails: OrderDetailsCustomerDetails;
  readonly requestedProducts: OrderDetailsRequestedProducts;
  readonly commentsTab: CommentsTab;
  readonly assignManagerModal: AssignManagerModal;
  readonly deliveryTab: DeliveryTab;
  readonly orderHistoryTab: OrderHistoryTab;
  readonly scheduleDeliveryPage: ScheduleDeliveryPage;
  readonly editCustomerModal: EditOrderCustomerModal;

  constructor(page: Page) {
    super(page);
    this.header = new OrderDetailsHeader(page);
    this.requestedProducts = new OrderDetailsRequestedProducts(page);
    this.commentsTab = new CommentsTab(page);
    this.assignManagerModal = new AssignManagerModal(page);
    this.deliveryTab = new DeliveryTab(page);
    this.orderHistoryTab = new OrderHistoryTab(page);
    this.scheduleDeliveryPage = new ScheduleDeliveryPage(page);
    this.editCustomerModal = new EditOrderCustomerModal(page);
    this.customerDetails = new OrderDetailsCustomerDetails(page);
  }

  // Modals
  readonly confirmationModal = new ConfirmationModal(this.page);
  processModal = this.confirmationModal;
  cancelModal = this.confirmationModal;
  reopenModal = this.confirmationModal;
  readonly editProductsModal = new EditProductsModal(this.page);

  @logStep("OPEN ORDER DETAILS BY ROUTE")
  async openByRoute(route: string) {
    await this.open(route);
  }

  @logStep("OPEN ORDER DETAILS BY ID")
  async openByOrderId(orderId: string) {
    // Site uses SPA routing: #/orders/{id}
    const route = `#/orders/${orderId}`;
    await this.open(route);
    await this.waitForSpinners();
  }

  @logStep("WAIT FOR ORDER DETAILS PAGE TO OPEN")
  async waitForOpened() {
    await expect(this.uniqueElement.first()).toBeVisible({ timeout: TIMEOUT_30_S });
    await this.waitForSpinners();
  }

  // Tabs (Delivery, History, Comments)
  readonly tabs = {
    root: this.page.locator("#order-details-tabs"),
    delivery: this.page.locator("#delivery-tab"),
    history: this.page.locator("#history-tab"),
    comments: this.page.locator("#comments-tab"),
    content: this.page.locator("#order-details-tabs-content"),
  } as const;

  @logStep("SWITCH TO DELIVERY TAB")
  async openDeliveryTab() {
    await this.tabs.delivery.click();
  }

  @logStep("SWITCH TO HISTORY TAB")
  async openHistoryTab() {
    await this.tabs.history.click();
  }

  @logStep("SWITCH TO COMMENTS TAB")
  async openCommentsTab() {
    await this.tabs.comments.click();
  }
  @logStep("CLICK PROCESS ORDER BUTTON")
  async clickProcess() {
    await this.processOrderButton.click();
    await this.processModal.waitForOpened();
  }

  @logStep("CLICK CANCEL ORDER BUTTON")
  async clickCancel() {
    await this.cancelOrderButton.click();
    await this.cancelModal.waitForOpened();
  }

  @logStep("CLICK REOPEN ORDER BUTTON")
  async clickReopen() {
    await this.reopenOrderButton.click();
    await this.reopenModal.waitForOpened();
  }

  @logStep("CLICK REFRESH ORDER BUTTON")
  async clickRefreshOrder() {
    await this.refreshOrderButton.click();
    await this.waitForSpinners();
  }
}
