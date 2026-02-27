import type { Download, TestInfo } from "@playwright/test";
import fs from "node:fs/promises";
import path from "node:path";
import { parseCsvToRecords, type CsvRecord } from "utils/files/csv.utils";

export type ExportedFile =
  | { format: "csv"; filePath: string; data: CsvRecord[] }
  | { format: "json"; filePath: string; data: unknown };

const extOf = (fileName: string): string => path.extname(fileName).toLowerCase();

export const saveDownloadToTestOutput = async (download: Download, testInfo: TestInfo): Promise<string> => {
  const suggested = download.suggestedFilename();
  const outPath = testInfo.outputPath(suggested);
  await download.saveAs(outPath);
  return outPath;
};

export const parseDownloadedExport = async (download: Download, testInfo: TestInfo): Promise<ExportedFile> => {
  const suggested = download.suggestedFilename();
  const filePath = await saveDownloadToTestOutput(download, testInfo);
  const text = await fs.readFile(filePath, "utf-8");

  const ext = extOf(suggested);
  if (ext === ".json") {
    return { format: "json", filePath, data: JSON.parse(text) as unknown };
  }

  // default/fallback: treat as CSV
  return { format: "csv", filePath, data: parseCsvToRecords(text) };
};
