#!/usr/bin/env npx tsx
/**
 * List documents on reMarkable
 *
 * Usage:
 *   npx tsx list.ts              # List all documents
 *   npx tsx list.ts --search "query"  # Search by name
 *   npx tsx list.ts --refresh    # Force refresh from cloud
 *   npx tsx list.ts --json       # Output as JSON
 */

import { initApi, findDocuments, getFolders, getPath, safeName } from "./common.js";
import type { Entry } from "rmapi-js";

interface ListOptions {
  search?: string;
  refresh?: boolean;
  json?: boolean;
}

function parseArgs(): ListOptions {
  const args = process.argv.slice(2);
  const options: ListOptions = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--search" && args[i + 1]) {
      options.search = args[++i];
    } else if (args[i] === "--refresh") {
      options.refresh = true;
    } else if (args[i] === "--json") {
      options.json = true;
    }
  }

  return options;
}

async function main() {
  const options = parseArgs();

  const api = await initApi();
  const items = await api.listItems(options.refresh);

  // Filter to documents only for search
  let documents: Entry[];
  if (options.search) {
    documents = findDocuments(items, options.search);
  } else {
    documents = items.filter((i) => i.type === "DocumentType");
  }

  const folders = getFolders(items);

  if (options.json) {
    // JSON output
    const output = documents.map((doc) => ({
      name: doc.visibleName,
      hash: doc.hash,
      id: doc.id,
      parent: doc.parent,
      path: getPath(doc, folders),
    }));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  // Human-readable output
  if (options.search) {
    console.log(`\nSearch results for "${options.search}":`);
    console.log("─".repeat(50));
  } else {
    console.log("\nreMarkable Documents:");
    console.log("─".repeat(50));
  }

  if (documents.length === 0) {
    console.log("No documents found.");
    return;
  }

  // Group by folder
  const rootDocs: Entry[] = [];
  const folderDocs = new Map<string, Entry[]>();

  for (const doc of documents) {
    const parent = doc.parent || "";
    if (!parent || parent === "") {
      rootDocs.push(doc);
    } else if (parent === "trash") {
      // Skip trashed documents unless searching
      if (options.search) {
        console.log(`  [TRASH] ${doc.visibleName}`);
      }
    } else {
      if (!folderDocs.has(parent)) {
        folderDocs.set(parent, []);
      }
      folderDocs.get(parent)!.push(doc);
    }
  }

  // Print root documents
  if (rootDocs.length > 0) {
    console.log("\n/ (root)");
    for (const doc of rootDocs.sort((a, b) => a.visibleName.localeCompare(b.visibleName))) {
      console.log(`  ${doc.visibleName}`);
    }
  }

  // Print folder documents
  for (const [folderId, docs] of folderDocs) {
    const folder = folders.get(folderId);
    const folderName = folder?.visibleName || folderId;
    const path = folder ? getPath(folder, folders) : "";
    const fullPath = path ? `${path}/${folderName}` : folderName;

    console.log(`\n/${fullPath}/`);
    for (const doc of docs.sort((a, b) => a.visibleName.localeCompare(b.visibleName))) {
      console.log(`  ${doc.visibleName}`);
    }
  }

  console.log(`\n${documents.length} document(s) total`);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
