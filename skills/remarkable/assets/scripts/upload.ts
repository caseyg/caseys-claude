#!/usr/bin/env npx tsx
/**
 * Upload PDF or EPUB to reMarkable
 *
 * Usage:
 *   npx tsx upload.ts <file.pdf|file.epub>
 *   npx tsx upload.ts <file.pdf> --name "Custom Name"
 *   npx tsx upload.ts <file.pdf> --folder "Folder Name"
 */

import { initApi, findDocuments, safeName } from "./common.js";
import { readFile } from "fs/promises";
import { basename } from "path";

interface UploadOptions {
  filePath: string;
  name?: string;
  folder?: string;
}

function parseArgs(): UploadOptions {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error("Usage: npx tsx upload.ts <file.pdf|file.epub> [--name 'Name'] [--folder 'Folder']");
    process.exit(1);
  }

  const options: UploadOptions = {
    filePath: args[0],
  };

  for (let i = 1; i < args.length; i++) {
    if (args[i] === "--name" && args[i + 1]) {
      options.name = args[++i];
    } else if (args[i] === "--folder" && args[i + 1]) {
      options.folder = args[++i];
    }
  }

  return options;
}

async function main() {
  const options = parseArgs();
  const { filePath, name, folder } = options;

  // Validate file extension
  const ext = filePath.toLowerCase().split(".").pop();
  if (ext !== "pdf" && ext !== "epub") {
    console.error("Error: Only PDF and EPUB files are supported");
    process.exit(1);
  }

  // Determine document name
  const docName = name || basename(filePath).replace(/\.(pdf|epub)$/i, "");

  console.log(`Uploading: ${filePath}`);
  console.log(`Name: ${docName}`);

  // Read file
  let buffer: Uint8Array;
  try {
    const fileBuffer = await readFile(filePath);
    buffer = new Uint8Array(fileBuffer);
  } catch (error) {
    console.error(`Error reading file: ${filePath}`);
    process.exit(1);
  }

  // Initialize API
  const api = await initApi();

  // Find folder if specified
  let parentId: string | undefined;
  if (folder) {
    const items = await api.listItems();
    const folders = items.filter((i) => i.type === "CollectionType");
    const match = folders.find(
      (f) => f.visibleName.toLowerCase() === folder.toLowerCase()
    );

    if (match) {
      parentId = match.id;
      console.log(`Folder: ${match.visibleName}`);
    } else {
      console.error(`Folder not found: ${folder}`);
      console.error("Available folders:");
      folders.forEach((f) => console.error(`  - ${f.visibleName}`));
      process.exit(1);
    }
  }

  // Upload
  try {
    let entry;
    if (parentId) {
      // Use low-level API for folder placement
      if (ext === "pdf") {
        entry = await api.putPdf(docName, buffer, { parent: parentId });
      } else {
        entry = await api.putEpub(docName, buffer, { parent: parentId });
      }
    } else {
      // Use simple API for root
      if (ext === "pdf") {
        entry = await api.uploadPdf(docName, buffer);
      } else {
        entry = await api.uploadEpub(docName, buffer);
      }
    }

    console.log("\nUpload successful!");
    console.log(`  Name: ${entry.visibleName}`);
    console.log(`  Hash: ${entry.hash}`);
    console.log(`  ID: ${entry.id}`);
  } catch (error) {
    if (error instanceof Error) {
      console.error(`Upload failed: ${error.message}`);

      // Check for GenerationError (concurrent edit)
      if (error.name === "GenerationError") {
        console.error("Concurrent edit detected. Please try again.");
      }
    }
    process.exit(1);
  }
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
