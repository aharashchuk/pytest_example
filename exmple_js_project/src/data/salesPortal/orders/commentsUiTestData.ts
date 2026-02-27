export interface ICommentUiCase {
  title: string;
  text: string;
  expectedError?: string;
}

export const CREATE_COMMENT_POSITIVE_CASES: ICommentUiCase[] = [
  {
    title: "Add single-character comment",
    text: "A",
  },
  {
    title: "Add short comment with multiple words",
    text: "This is a test comment",
  },
  {
    title: "Add comment with punctuation marks",
    text: "Great progress! Let's ship it soon.",
  },
  {
    title: "Add 250-character comment (max length)",
    text: "a".repeat(250),
  },
  {
    title: "Add comment with numbers",
    text: "Order #1234 ready",
  },
];

export const CREATE_COMMENT_NEGATIVE_CASES: ICommentUiCase[] = [
  {
    title: "Comment with 251 characters should show error",
    text: "a".repeat(251),
    expectedError: "Comment should be in range 1-250 and without < or > symbols",
  },
  {
    title: "Comment with '<' symbol should show error",
    text: "Check < this value",
    expectedError: "Comment should be in range 1-250 and without < or > symbols",
  },
  {
    title: "Comment with '>' symbol should show error",
    text: "Value > threshold",
    expectedError: "Comment should be in range 1-250 and without < or > symbols",
  },
];
