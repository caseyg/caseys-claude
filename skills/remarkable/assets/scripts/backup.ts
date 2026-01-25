#!/usr/bin/env npx tsx
/**
 * Backup all reMarkable documents
 *
 * Usage:
 *   npx tsx backup.ts
 *   npx tsx backup.ts --output ./backups
 *   npx tsx backup.ts --include-original  # Also download original PDFs
 */

import { initApi, safeName, today, getFolders, getPath } from "./common.js";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";
import type { Entry } from "rmapi-js";

interface BackupOptions {
  output?: string;
  includeOriginal?: boolean;
}

function parseArgs(): BackupOptions {
  const args = process.argv.slice(2);
  const options: BackupOptions = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output" && args[i + 1]) {
      options.output = args[++i];
    } else if (args[i] === "--include-original") {
      options.includeOriginal = true;
    }
  }

  return options;
}

interface ManifestEntry {
  name: string;
  hash: string;
  parent: string | undefined;
  path: string;
  file: string;
  originalFile?: string;
  error?: string;
}

interface Manifest {
  backupDate: string;
  documentCount: number;
  successCount: number;
  errorCount: number;
  documents: ManifestEntry[];
}

async function main() {
  const options = parseArgs();

  console.log("Starting reMarkable backup...\n");

  // Initialize API
  const api = await initApi();

  // Get all documents (force refresh)
  console.log("Fetching document list...");
  const items = await api.listItems(true);
  const documents = items.filter((i) => i.type === "DocumentType" && i.parent !== "trash");
  const folders = getFolders(items);

  console.log(`Found ${documents.length} documents\n`);

  // Create backup directory
  const backupDir = options.output || join("data", "downloads", `${today()}-backup`);
  await mkdir(backupDir, { recursive: true });

  const manifest: Manifest = {
    backupDate: new Date().toISOString(),
    documentCount: documents.length,
    successCount: 0,
    errorCount: 0,
    documents: [],
  };

  // Download each document
  for (let i = 0; i < documents.length; i++) {
    const doc = documents[i];
    const progress = `[${i + 1}/${documents.length}]`;
    const path = getPath(doc, folders);

    const entry: ManifestEntry = {
      name: doc.visibleName,
      hash: doc.hash,
      parent: doc.parent,
      path,
      file: "",
    };

    try {
      process.stdout.write(`${progress} ${doc.visibleName}...`);

      // Download ZIP archive
      const zipData = await api.getDocument(doc.hash);
      const safeDocName = safeName(doc.visibleName);
      const fileName = `${safeDocName}-${doc.hash.slice(0, 8)}.zip`;
      const filePath = join(backupDir, fileName);
      await writeFile(filePath, zipData);
      entry.file = fileName;

      // Download original if requested
      if (options.includeOriginal) {
        try {
          const pdfData = await api.getPdf(doc.hash);
          const originalFileName = `${safeDocName}-${doc.hash.slice(0, 8)}-original.pdf`;
          await writeFile(join(backupDir, originalFileName), pdfData);
          entry.originalFile = originalFileName;
        } catch {
          // No original PDF available (notebook or EPUB)
          try {
            const epubData = await api.getEpub(doc.hash);
            const originalFileName = `${safeDocName}-${doc.hash.slice(0, 8)}-original.epub`;
            await writeFile(join(backupDir, originalFileName), epubData);
            entry.originalFile = originalFileName;
          } catch {
            // Pure notebook, no original
          }
        }
      }

      console.log(" done");
      manifest.successCount++;
    } catch (error) {
      console.log(" FAILED");
      entry.error = error instanceof Error ? error.message : "Unknown error";
      manifest.errorCount++;
    }

    manifest.documents.push(entry);

    // Rate limiting - small delay between downloads
    await new Promise((r) => setTimeout(r, 200));
  }

  // Save manifest
  const manifestPath = join(backupDir, "manifest.json");
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2));

  // Summary
  console.log("\n" + "=".repeat(50));
  console.log("Backup Complete!");
  console.log("=".repeat(50));
  console.log(`Location: ${backupDir}`);
  console.log(`Total documents: ${manifest.documentCount}`);
  console.log(`Successful: ${manifest.successCount}`);
  if (manifest.errorCount > 0) {
    console.log(`Failed: ${manifest.errorCount}`);
    console.log("\nFailed documents:");
    manifest.documents
      .filter((d) => d.error)
      .forEach((d) => console.log(`  - ${d.name}: ${d.error}`));
  }
  console.log(`\nManifest: ${manifestPath}`);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
