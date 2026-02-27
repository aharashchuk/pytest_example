import { defineConfig, devices } from "@playwright/test";
import dotenv from "dotenv";
import path from "path";

// Load environment variables from the appropriate .env file.
// Default: .env; Dev: .env.dev when TEST_ENV=dev
const TEST_ENV = process.env.TEST_ENV?.trim();
const envFile = TEST_ENV === "dev" ? ".env.dev" : ".env";
dotenv.config({ path: path.resolve(process.cwd(), envFile) });

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// import dotenv from 'dotenv';
// import path from 'path';
// dotenv.config({ path: path.resolve(__dirname, '.env') });
/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  //globalTeardown: require.resolve("./src/config/global.teardown"),
  testDir: "./src/tests",
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 1,
  /* Opt out of parallel tests on CI. */
  workers: 5,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ["html"],
    [
      "allure-playwright",
      {
        suiteTitle: false,
        environmentInfo: {
          ENV: TEST_ENV ?? "default",
          UI_URL: process.env.SALES_PORTAL_URL,
          API_URL: process.env.SALES_PORTAL_API_URL,
        },
      },
    ],
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('')`. */
    // baseURL: 'http://localhost:3000',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: "on",
    screenshot: "only-on-failure",
    video: "on-first-retry",
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: "setup",
      use: { ...devices["Desktop Chrome"] },
      testDir: "src/tests/ui",
      testMatch: /auth\.setup\.ts/,
    },
    {
      name: "sales-portal-ui",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1920, height: 1080 },
        storageState: "src/.auth/user.json",
      },
      dependencies: ["setup"],
      testDir: "src/tests/ui",
    },
    {
      name: "sales-portal-api",
      use: {
        ...devices["Desktop Chrome"],
      },
      testDir: "src/tests/api",
    },
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"], headless: true },
      testDir: "src/tests/ui",
    },

    // {
    //   name: "firefox",
    //   use: { ...devices["Desktop Firefox"] },
    // },

    // {
    //   name: "webkit",
    //   use: { ...devices["Desktop Safari"] },
    // },

    /* Test against mobile viewports. */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },

    /* Test against branded browsers. */
    // {
    //   name: 'Microsoft Edge',
    //   use: { ...devices['Desktop Edge'], channel: 'msedge' },
    // },
    // {
    //   name: 'Google Chrome',
    //   use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    // },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
