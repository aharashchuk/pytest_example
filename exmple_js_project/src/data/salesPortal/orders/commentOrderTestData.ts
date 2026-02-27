import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { ICommentOrderCase } from "data/types/order.types";
import { faker } from "@faker-js/faker";
import { ObjectId } from "bson";

export const commentOrderPositiveCases: ICommentOrderCase[] = [
  {
    title: "Add 1-char comment",
    text: faker.string.alphanumeric({ length: 1 }),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Add 250-char comment",
    text: faker.string.alphanumeric({ length: 250 }),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Add regular sentence with punctuation",
    text: faker.lorem.sentence(7),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const commentOrderNegativeCases: ICommentOrderCase[] = [
  {
    title: "Empty comment is rejected",
    text: "",
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Too long comment (251) is rejected",
    text: faker.string.alphanumeric({ length: 251 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Comment with '<' is rejected",
    text: "Please check < invalid tag",
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Comment with '>' is rejected",
    text: "Ensure > threshold before ship",
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];

export const deleteOrderCommentPositiveCases: ICommentOrderCase[] = [
  {
    title: "Delete existing comment",
    text: faker.lorem.sentence(5),
    expectedStatus: STATUS_CODES.DELETED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const deleteOrderCommentNegativeCases: ICommentOrderCase[] = [
  {
    title: "Non-existing commentId rejected",
    _id: new ObjectId().toString(),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Invalid ID format rejected",
    _id: "invalid-comment-id",
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Empty comment ID is rejected",
    _id: new ObjectId().toString(),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];
