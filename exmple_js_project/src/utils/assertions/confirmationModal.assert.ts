import { expect, type Locator } from "@playwright/test";
import type { ModalCopy } from "data/salesPortal/notifications";

export type ConfirmationModal = {
  title: Locator;
  confirmationMessage: Locator;
  confirmButton: Locator;
};

export async function assertConfirmationModal(modal: ConfirmationModal, copy: ModalCopy) {
  await expect(modal.title).toHaveText(copy.title);
  await expect(modal.confirmationMessage).toHaveText(copy.body);
  await expect(modal.confirmButton).toHaveText(copy.actionButton);
}
