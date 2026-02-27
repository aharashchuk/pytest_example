/**
 * Masks sensitive data values in a JSON string by replacing them with "[REDACTED]".
 *
 * This function searches for specific sensitive field names (password, authorization, Authorization)
 * and replaces their values with a redacted placeholder while preserving the JSON structure.
 *
 * @param {string} data - The input string containing potentially sensitive data (typically JSON)
 * @returns {string} The input string with sensitive values replaced by "[REDACTED]"
 *
 * @example
 * const masked = maskSecrets(data); // '{"Authorization": "[REDACTED]"}'
 */
export const maskSecrets = (data: string): string => {
  const PATTERN = /"(password|authorization|Authorization)":\s*(?:"[^"]*"|'[^']*'|\d+)/;
  const REG_EXP = new RegExp(PATTERN, "gi");

  return data.replace(REG_EXP, '"$1": "[REDACTED]"');
};
