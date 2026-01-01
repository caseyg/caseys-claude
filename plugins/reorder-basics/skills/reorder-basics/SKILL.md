# Reorder Basics

A skill for quickly reordering items from Amazon's Buy Again page using browser automation and 1Password integration.

## Description

This skill should be used when the user asks to "reorder", "buy again", or "repurchase" an item from Amazon. It automates the entire process of logging in, finding the item, confirming details, and completing the purchase.

## Trigger Phrases

- "reorder [item]"
- "buy [item] again from Amazon"
- "repurchase [item]"
- "order more [item]"
- "/reorder-basics [item]"

## Prerequisites

1. **1Password CLI** must be installed and configured (`op` command available)
2. **dev-browser plugin** must be installed (`/plugin install dev-browser@dev-browser-marketplace`)
3. Amazon account credentials stored in 1Password with the tag or title containing "Amazon"

### Installing 1Password CLI

If `op` command is not found, install it:

```bash
brew install --cask 1password-cli
```

Then the user needs to enable CLI integration in the 1Password app:
1. Open 1Password → Settings → Developer
2. Enable "Integrate with 1Password CLI"

## Workflow

### Step 1: Get Amazon Credentials from 1Password

Use the 1Password CLI to retrieve Amazon credentials:

```bash
op item get "Amazon" --fields username,password --format json
```

If multiple Amazon entries exist, list them and ask the user which one to use:

```bash
op item list --tags amazon --format json
```

### Step 2: Navigate to Amazon and Login

Use dev-browser to automate the login flow:

1. Navigate to https://www.amazon.com/gp/buyagain
2. Amazon will redirect to sign-in if not logged in
3. Take a snapshot to see the current page state
4. If on sign-in page:
   - Enter the email/username in the email field
   - Click "Continue" button
   - Enter password on the next page
   - Click "Sign in"

**Handling 2FA (OTP):**

If Amazon prompts for a one-time password, fetch it from 1Password:

```bash
op item get "Amazon" --otp
```

This returns the current TOTP code. Enter it in the OTP field.

**Tip:** Check the "Don't require OTP on this browser" checkbox if available to skip 2FA on future sessions.

### Step 3: Navigate to Buy Again Page

1. After login, navigate to: https://www.amazon.com/gp/buyagain
2. Take a snapshot to see available items

### Step 4: Search and Match the Requested Item

1. Look for the "Search your orders" input on the Buy Again page
2. Type the item name in the search field
3. If search doesn't yield results, scroll down the page
4. Take snapshots to find items matching the user's request
5. Use fuzzy matching on product titles to find the best match

**Note:** dev-browser maintains persistent state, so you can navigate and interact without re-establishing context between steps.

**Matching Strategy:**
- Extract product names from the snapshot
- Compare against user's requested item
- Consider partial matches (e.g., "paper towels" matches "Bounty Paper Towels")
- If multiple matches, present options to the user

### Step 5: Confirm Item Details with User

Before proceeding, use `AskUserQuestion` to confirm:

1. **Product Name**: The full product title
2. **Price**: Current price shown
3. **Quantity**: Default quantity (usually 1)
4. **Shipping**: Estimated delivery date/shipping method

### Step 6: Complete the Purchase

If user confirms:

1. Click the "Buy Now" or "Add to Cart" button for the item
2. If "Buy Now" is available, it will go directly to checkout
3. If using cart, navigate to cart and click "Proceed to checkout"
4. On checkout page, verify shipping address and payment method
5. **CRITICAL**: Ask user for final confirmation before clicking "Place your order"
6. Click "Place your order" only after explicit user approval
7. Capture order confirmation details

### Step 7: Report Success

Provide the user with:
- Confirmation that order was placed (look for "Order placed, thanks!" heading)
- Expected delivery date
- Total amount charged
- Shipping address used

**Note:** The order confirmation number is sent via email rather than displayed prominently on the confirmation page.

## Safety Measures

1. **Always confirm before purchase**: Never click "Place your order" without explicit user approval
2. **Price verification**: Alert user if price seems significantly different from expected
3. **Address verification**: Show shipping address before completing order
4. **Screenshot evidence**: Take screenshots at key steps for user reference

## Error Handling

### Login Issues
- If 2FA is required, fetch OTP from 1Password with `op item get "Amazon" --otp`
- If CAPTCHA appears, take a screenshot and ask user to complete it manually
- If login fails, report error and suggest manual login

### Item Not Found
- If exact match not found, show similar items
- If no matches, suggest checking the spelling or browsing manually

### Checkout Issues
- If payment method needs updating, alert user
- If address needs confirmation, show options and ask user to choose

## Tools Reference

This skill uses the **dev-browser** plugin for browser automation. Invoke it via the `Skill` tool:

```
Skill: dev-browser:dev-browser
```

dev-browser provides:
- Navigation and page interaction
- Form filling and clicking
- DOM snapshots optimized for AI analysis
- Persistent browser state across interactions
- Screenshot capture

And these Claude Code tools:

| Tool | Purpose |
|------|---------|
| `Bash` | Run 1Password CLI commands |
| `AskUserQuestion` | Confirm details with user |
| `Skill` | Invoke dev-browser for browser automation |
