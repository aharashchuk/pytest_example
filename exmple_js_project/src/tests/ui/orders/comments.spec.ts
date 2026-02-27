import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import {
  CREATE_COMMENT_POSITIVE_CASES,
  CREATE_COMMENT_NEGATIVE_CASES,
} from "data/salesPortal/orders/commentsUiTestData";

test.describe("[UI][Orders][Comments]", () => {
  test.beforeEach(async ({ cleanup }) => {
    // Activate API cleanup fixture teardown (calls OrdersApiService.fullDelete).
    void cleanup;
  });

  test.describe("Create", () => {
    for (const testCase of CREATE_COMMENT_POSITIVE_CASES) {
      test(
        testCase.title,
        { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
        async ({ loginApiService, ordersApiService, commentsUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderInProcess(token, 1);

          await commentsUIService.openOrderComments(order._id);
          await commentsUIService.orderDetailsPage.commentsTab.expectCreateDisabled();
          await commentsUIService.addComment(testCase.text);

          await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(1);
        },
      );
    }
  });

  test.describe("Not create", () => {
    for (const testCase of CREATE_COMMENT_NEGATIVE_CASES) {
      test(
        testCase.title,
        { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
        async ({ loginApiService, ordersApiService, commentsUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderInProcess(token, 1);

          await commentsUIService.openOrderComments(order._id);
          await commentsUIService.orderDetailsPage.commentsTab.fillComment(testCase.text);

          await expect(commentsUIService.orderDetailsPage.commentsTab.error).toBeVisible();
          await expect(commentsUIService.orderDetailsPage.commentsTab.error).toHaveText(testCase.expectedError!);
          await commentsUIService.orderDetailsPage.commentsTab.expectCreateDisabled();
          await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(0);
        },
      );
    }
  });

  test(
    "Add multiple comments to same order",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.SMOKE] },
    async ({ loginApiService, ordersApiService, commentsUIService }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 1);

      await commentsUIService.openOrderComments(order._id);

      const comments = ["First comment", "Second comment", "Third comment"];

      for (let i = 0; i < comments.length; i++) {
        await commentsUIService.addComment(comments[i]!);
        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(i + 1);
      }

      await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(3);
      await expect(commentsUIService.orderDetailsPage.commentsTab.commentText.nth(0)).toHaveText(comments[2]!);
      await expect(commentsUIService.orderDetailsPage.commentsTab.commentText.nth(1)).toHaveText(comments[1]!);
      await expect(commentsUIService.orderDetailsPage.commentsTab.commentText.nth(2)).toHaveText(comments[0]!);
    },
  );

  test(
    "Create button is disabled for empty comment",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.SMOKE] },
    async ({ loginApiService, ordersApiService, commentsUIService }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 1);

      await commentsUIService.openOrderComments(order._id);

      await commentsUIService.orderDetailsPage.commentsTab.expectTextareaEmpty();
      await commentsUIService.orderDetailsPage.commentsTab.expectCreateDisabled();

      await commentsUIService.orderDetailsPage.commentsTab.fillComment("Some text");
      await commentsUIService.orderDetailsPage.commentsTab.expectCreateEnabled();

      await commentsUIService.orderDetailsPage.commentsTab.fillComment("");
      await commentsUIService.orderDetailsPage.commentsTab.expectCreateDisabled();
    },
  );

  test.describe("Delete", () => {
    test(
      "Delete first comment",
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ loginApiService, ordersApiService, commentsUIService }) => {
        const token = await loginApiService.loginAsAdmin();
        const order = await ordersApiService.createOrderInProcess(token, 1);

        // Add comments via API
        await ordersApiService.addComment(token, order._id, "Comment 1");
        await ordersApiService.addComment(token, order._id, "Comment 2");
        await ordersApiService.addComment(token, order._id, "Comment 3");

        await commentsUIService.openOrderComments(order._id);

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(3);

        await commentsUIService.deleteFirstComment();

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(2);
      },
    );

    test(
      "Delete last comment",
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ loginApiService, ordersApiService, commentsUIService }) => {
        const token = await loginApiService.loginAsAdmin();
        const order = await ordersApiService.createOrderInProcess(token, 1);

        await ordersApiService.addComment(token, order._id, "First");
        await ordersApiService.addComment(token, order._id, "Last");

        await commentsUIService.openOrderComments(order._id);

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(2);

        await commentsUIService.deleteLastComment();

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(1);
      },
    );

    test(
      "Delete all comments one by one",
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ loginApiService, ordersApiService, commentsUIService }) => {
        const token = await loginApiService.loginAsAdmin();
        const order = await ordersApiService.createOrderInProcess(token, 1);

        // Add 3 comments via API
        await ordersApiService.addComment(token, order._id, "Comment 1");
        await ordersApiService.addComment(token, order._id, "Comment 2");
        await ordersApiService.addComment(token, order._id, "Comment 3");

        await commentsUIService.openOrderComments(order._id);

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(3);

        await commentsUIService.deleteAllComments();

        await expect(commentsUIService.orderDetailsPage.commentsTab.commentCards).toHaveCount(0);
      },
    );
  });
});
