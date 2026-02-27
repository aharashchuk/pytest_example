import { ICredentials } from "data/types/credentials.types";
import dotenv from "dotenv";

dotenv.config();
export const SALES_PORTAL_URL = process.env.SALES_PORTAL_URL!;
export const SALES_PORTAL_API_URL = process.env.SALES_PORTAL_API_URL!;

export const credentials: ICredentials = {
  username: process.env.USER_NAME!,
  password: process.env.USER_PASSWORD!,
};

export const MANAGER_IDS: string[] = JSON.parse(process.env.MANAGER_IDS!);
