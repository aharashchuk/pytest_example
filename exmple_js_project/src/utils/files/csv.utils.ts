export type CsvRecord = Record<string, string>;

const stripBom = (value: string): string => value.replace(/^\uFEFF/, "");

const normalizeHeaders = (rawHeaders: string[]): string[] => {
  const seen = new Map<string, number>();

  return rawHeaders.map((h, idx) => {
    let base = stripBom(h).trim();
    if (!base) base = `__col_${idx + 1}`;

    const prev = seen.get(base) ?? 0;
    const next = prev + 1;
    seen.set(base, next);

    return next === 1 ? base : `${base}__${next}`;
  });
};

const detectDelimiter = (headerLine: string): string => {
  const commaCount = (headerLine.match(/,/g) ?? []).length;
  const semicolonCount = (headerLine.match(/;/g) ?? []).length;
  return semicolonCount > commaCount ? ";" : ",";
};

const parseCsvToRows = (text: string, delimiter: string): string[][] => {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const char = text[i]!;

    if (inQuotes) {
      if (char === '"') {
        const next = text[i + 1];
        if (next === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += char;
      }
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      continue;
    }

    if (char === "\r") continue;

    if (char === delimiter) {
      row.push(field);
      field = "";
      continue;
    }

    if (char === "\n") {
      row.push(field);
      field = "";
      rows.push(row);
      row = [];
      continue;
    }

    field += char;
  }

  // flush last field/row
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }

  // drop trailing empty row
  if (rows.length > 0 && rows[rows.length - 1]?.every((c) => c.trim() === "")) {
    rows.pop();
  }

  return rows;
};

export const parseCsvToRecords = (text: string): CsvRecord[] => {
  const trimmed = text.trim();
  if (!trimmed) return [];

  const firstLine = trimmed.split(/\r?\n/, 1)[0] ?? "";
  const delimiter = detectDelimiter(firstLine);

  const rows = parseCsvToRows(trimmed, delimiter);
  if (rows.length === 0) return [];

  const headers = normalizeHeaders((rows[0] ?? []).map((h) => h));
  const records: CsvRecord[] = [];

  for (const row of rows.slice(1)) {
    if (row.every((c) => c.trim() === "")) continue;

    const record: CsvRecord = {};
    for (let i = 0; i < headers.length; i++) {
      const key = headers[i];
      if (key === undefined) continue;
      record[key] = (row[i] ?? "").trim();
    }
    records.push(record);
  }

  return records;
};
