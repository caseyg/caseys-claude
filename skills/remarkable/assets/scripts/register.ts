#!/usr/bin/env npx tsx
/**
 * Register a new device with reMarkable cloud
 *
 * Usage: npx tsx register.ts <8-character-code>
 *
 * 1. Go to https://my.remarkable.com/device/browser/connect
 * 2. Copy the 8-character code displayed
 * 3. Run this script with the code
 * 4. Device token will be stored in 1Password
 */

import { register } from "rmapi-js";
import { storeDeviceToken } from "./common.js";

async function main() {
  const code = process.argv[2];

  if (!code || code.length !== 8) {
    console.error("Usage: npx tsx register.ts <8-character-code>");
    console.error("");
    console.error("To get a code:");
    console.error("1. Go to https://my.remarkable.com/device/browser/connect");
    console.error("2. Copy the 8-character code displayed");
    process.exit(1);
  }

  console.log(`Registering with code: ${code}`);

  try {
    // Exchange code for device token
    const deviceToken = await register(code);

    console.log("Registration successful!");
    console.log(`Device token: ${deviceToken.slice(0, 20)}...`);

    // Store in 1Password
    console.log("\nStoring in 1Password...");

    if (storeDeviceToken(deviceToken)) {
      console.log('Stored in 1Password item "Remarkable"');
      console.log("\nSetup complete! You can now use the reMarkable skill.");
    } else {
      console.error("Failed to store in 1Password. Store manually:");
      console.error("  Item: Remarkable");
      console.error("  Field: device_token");
      console.error(`  Value: ${deviceToken}`);
      process.exit(1);
    }
  } catch (error) {
    if (error instanceof Error) {
      if (error.message.includes("401")) {
        console.error("Invalid or expired code. Get a new code from:");
        console.error("https://my.remarkable.com/device/browser/connect");
      } else {
        console.error(`Registration failed: ${error.message}`);
      }
    }
    process.exit(1);
  }
}

main();
