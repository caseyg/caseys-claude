/**
 * Common utilities for reMarkable API operations
 *
 * Usage: import { getDeviceToken, initApi, findDocument } from "./common.js"
 */

import { remarkable, type RemarkableApi, type Entry } from "rmapi-js";
import { execFileSync } from "child_process";

// 1Password item name for Remarkable API credentials
// Override with OP_REMARKABLE_ITEM env var if you have naming conflicts
const OP_ITEM_NAME = process.env.OP_REMARKABLE_ITEM || "Remarkable";

/**
 * Retrieve device token from 1Password
 * @returns Device token string
 * @throws Error if 1Password item not found
 */
export async function getDeviceToken(): Promise<string> {
  try {
    const result = execFileSync("op", ["item", "get", OP_ITEM_NAME, "--fields", "device_token", "--reveal"], {
      encoding: "utf-8",
    });
    return result.trim();
  } catch (error) {
    throw new Error(
      "Device token not found in 1Password. Run registration first:\n" +
        "1. Go to https://my.remarkable.com/device/browser/connect\n" +
        "2. Get the 8-character code\n" +
        "3. Run: npx tsx skills/remarkable/assets/scripts/register.ts <code>"
    );
  }
}

/**
 * Store device token in 1Password (create or update)
 * @param token - Device token to store
 * @returns true if successful
 */
export function storeDeviceToken(token: string): boolean {
  try {
    // Try to update existing item first
    execFileSync("op", ["item", "edit", "Remarkable", `device_token=${token}`], {
      encoding: "utf-8",
      stdio: "pipe",
    });
    return true;
  } catch {
    try {
      // Create new item if it doesn't exist
      execFileSync("op", ["item", "create", "--category=API Credential", "--title=Remarkable", `device_token=${token}`], {
        encoding: "utf-8",
        stdio: "pipe",
      });
      return true;
    } catch {
      return false;
    }
  }
}

/**
 * Initialize reMarkable API with device token from 1Password
 * @returns Initialized API instance
 */
export async function initApi(): Promise<RemarkableApi> {
  const deviceToken = await getDeviceToken();
  return remarkable(deviceToken);
}

/**
 * Fuzzy search for documents by name
 * @param items - List of entries from api.listItems()
 * @param query - Search query
 * @returns Matching documents sorted by relevance
 */
export function findDocuments(items: Entry[], query: string): Entry[] {
  const queryLower = query.toLowerCase();
  return items
    .filter((item) => item.type === "DocumentType")
    .filter((item) => item.visibleName.toLowerCase().includes(queryLower))
    .sort((a, b) => {
      const aName = a.visibleName.toLowerCase();
      const bName = b.visibleName.toLowerCase();

      // Exact match first
      if (aName === queryLower) return -1;
      if (bName === queryLower) return 1;

      // Prefix match second
      if (aName.startsWith(queryLower) && !bName.startsWith(queryLower)) return -1;
      if (bName.startsWith(queryLower) && !aName.startsWith(queryLower)) return 1;

      // Alphabetical for contains matches
      return aName.localeCompare(bName);
    });
}

/**
 * Find folders from item list
 * @param items - List of entries from api.listItems()
 * @returns Map of folder ID to folder entry
 */
export function getFolders(items: Entry[]): Map<string, Entry & { children: Entry[] }> {
  const folders = new Map<string, Entry & { children: Entry[] }>();

  for (const item of items) {
    if (item.type === "CollectionType") {
      folders.set(item.id, { ...item, children: [] });
    }
  }

  // Add documents to their parent folders
  for (const item of items) {
    if (item.type === "DocumentType" && item.parent && folders.has(item.parent)) {
      folders.get(item.parent)!.children.push(item);
    }
  }

  return folders;
}

/**
 * Build folder path string for a document
 * @param item - Document entry
 * @param folders - Folder map from getFolders()
 * @returns Path string like "Folder/Subfolder"
 */
export function getPath(item: Entry, folders: Map<string, Entry & { children: Entry[] }>): string {
  const parts: string[] = [];
  let current = item.parent;

  while (current && current !== "" && current !== "trash") {
    const folder = folders.get(current);
    if (folder) {
      parts.unshift(folder.visibleName);
      current = folder.parent;
    } else {
      break;
    }
  }

  return parts.join("/");
}

/**
 * Sanitize filename for filesystem
 * @param name - Original name
 * @returns Safe filename
 */
export function safeName(name: string): string {
  return name.replace(/[^a-zA-Z0-9-_. ]/g, "_").replace(/\s+/g, "_");
}

/**
 * Get today's date in YYYY-MM-DD format
 */
export function today(): string {
  return new Date().toISOString().split("T")[0];
}
