import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import prettierConfig from "eslint-config-prettier";
import prettierPlugin from "eslint-plugin-prettier";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ["src/**/*.{js,mjs,cjs,ts}"]
  },
  { 
    languageOptions: {
      globals: globals.node,
      parserOptions: {
      createDefaultProgram: true,
      project: './tsconfig.json',
    },
    },
  },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  prettierConfig,
  {
    plugins: { prettier: prettierPlugin },
    rules: {
      "prettier/prettier": ["error", { endOfLine: "auto", printWidth: 120, singleQuote: false }],
      "@typescript-eslint/no-unused-expressions": "off",
      "@typescript-eslint/no-explicit-any": "off",
      "no-empty-pattern": "off",
      "no-useless-escape": "off",
      eqeqeq: "error", // Enforce strict equality (=== instead of ==)
      "@typescript-eslint/no-floating-promises": "error"
    }
  },
  {
    ignores: ["**/node_modules/**", "**/dist/**", "eslint.config.mts", "lint-staged.config.js", "**/allure-results/**", "**/playwright-report/**"]
  }
];
