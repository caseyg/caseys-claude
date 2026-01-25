#!/usr/bin/env npx tsx
/**
 * Download document from reMarkable
 *
 * Usage:
 *   npx tsx download.ts "Document Name"
 *   npx tsx download.ts "Document Name" --output ./downloads
 *   npx tsx download.ts "Document Name" --original  # Also download original PDF
 *   npx tsx download.ts --hash abc123def456        # Download by hash
 */

import { initApi, findDocuments, safeName, today } from "./common.js";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";

interface DownloadOptions {
  query?: string;
  hash?: string;
  output?: string;
  original?: boolean;
}

function parseArgs(): DownloadOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: npx tsx download.ts "Document Name" [--output dir] [--original]');
    console.error('       npx tsx download.ts --hash <hash> [--output dir] [--original]');
    process.exit(1);
  }

  const options: DownloadOptions = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--hash" && args[i + 1]) {
      options.hash = args[++i];
    } else if (args[i] === "--output" && args[i + 1]) {
      options.output = args[++i];
    } else if (args[i] === "--original") {
      options.original = true;
    } else if (!args[i].startsWith("--")) {
      options.query = args[i];
    }
  }

  if (!options.query && !options.hash) {
    console.error("Error: Provide a document name or --hash");
    process.exit(1);
  }

  return options;
}

async function main() {
  const options = parseArgs();

  // Initialize API
  const api = await initApi();

  // Find document
  let docHash: string;
  let docName: string;

  if (options.hash) {
    docHash = options.hash;
    docName = options.hash.slice(0, 8);

    // Try to get the actual name from metadata
    try {
      const metadata = await api.getMetadata(docHash);
      docName = metadata.visibleName;
    } catch {
      // Use hash as name if metadata lookup fails
    }
  } else {
    const items = await api.listItems();
    const matches = findDocuments(items, options.query!);

    if (matches.length === 0) {
      console.error(`No documents found matching: ${options.query}`);
      process.exit(1);
    }

    if (matches.length > 1) {
      console.error(`Multiple documents found matching: ${options.query}`);
      console.error("Please be more specific or use --hash:");
      matches.slice(0, 10).forEach((m) => {
        console.error(`  "${m.visibleName}" (--hash ${m.hash})`);
      });
      process.exit(1);
    }

    docHash = matches[0].hash;
    docName = matches[0].visibleName;
  }

  console.log(`Downloading: ${docName}`);
  console.log(`Hash: ${docHash}`);

  // Create output directory
  const outputDir = options.output || join("data", "downloads", today());
  await mkdir(outputDir, { recursive: true });

  const safeDocName = safeName(docName);

  // Download full document as ZIP
  try {
    console.log("\nFetching document archive...");
    const zipData = await api.getDocument(docHash);
    const zipPath = join(outputDir, `${safeDocName}.zip`);
    await writeFile(zipPath, zipData);
    console.log(`Saved: ${zipPath}`);
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "HashNotFoundError") {
        console.error("Document not found. It may have been deleted.");
      } else {
        console.error(`Failed to download archive: ${error.message}`);
      }
    }
    process.exit(1);
  }

  // Download original PDF/EPUB if requested
  if (options.original) {
    try {
      console.log("\nFetching original PDF...");
      const pdfData = await api.getPdf(docHash);
      const pdfPath = join(outputDir, `${safeDocName}-original.pdf`);
      await writeFile(pdfPath, pdfData);
      console.log(`Saved: ${pdfPath}`);
    } catch {
      try {
        console.log("No PDF found, trying EPUB...");
        const epubData = await api.getEpub(docHash);
        const epubPath = join(outputDir, `${safeDocName}-original.epub`);
        await writeFile(epubPath, epubData);
        console.log(`Saved: ${epubPath}`);
      } catch {
        console.log("No original PDF or EPUB available (may be a notebook)");
      }
    }
  }

  console.log(`\nDownload complete. Files saved to: ${outputDir}`);
  console.log("\nTo render annotations, extract the ZIP and run:");
  console.log(`  unzip "${join(outputDir, safeDocName + ".zip")}" -d "${join(outputDir, safeDocName + "_extracted")}"`);
  console.log(`  python skills/remarkable/assets/scripts/render-annotations.py "${join(outputDir, safeDocName + "_extracted")}" "${join(outputDir, safeDocName + "-annotated.pdf")}"`);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
