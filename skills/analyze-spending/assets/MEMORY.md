# Spending Analysis Memory

This file tracks decisions, preferences, and learned patterns from spending analysis sessions.
Copy this template to `data/MEMORY.md` and customize.

---

## User Preferences

### Categories to Exclude from Analysis
<!-- Categories that should be excluded from spending totals (e.g., transfers, savings) -->
```yaml
excluded_categories:
  - "Payment, Transfer"
  - "Withdrawal"
```

### Subscriptions to Always Keep
<!-- Services marked as essential - won't be flagged for cancellation -->
```yaml
essential_subscriptions: []
  # - payee: "Cloud Backup Service"
  #   reason: "Essential for data protection"
  # - payee: "Password Manager"
  #   reason: "Security critical"
```

### Subscriptions on Watchlist
<!-- Services being monitored for potential cancellation -->
```yaml
watchlist: []
  # - payee: "Streaming Service"
  #   added: YYYY-MM-DD
  #   review_date: YYYY-MM-DD
  #   reason: "Haven't used in a while"
```

### Known Duplicates (Intentional)
<!-- Duplicate-looking subscriptions that are intentional -->
```yaml
intentional_duplicates: []
  # - payee: "News Subscription"
  #   reason: "One personal, one gift"
```

---

## Spending Targets

### Monthly Budget Goals
```yaml
budget_targets:
  # Entertainment: 200
  # Restaurants: 300
  # Coffee Shops: 100
  # Shopping: 500
```

### Subscription Budget
```yaml
subscription_budget:
  monthly_target: null  # Set a monthly cap, e.g., 200
  annual_target: null   # Set an annual cap, e.g., 2400
```

---

## Learned Patterns

### Merchant Aliases
<!-- Map different payee names to canonical names -->
```yaml
merchant_aliases: {}
  # "AMZN Mktp US": "Amazon"
  # "SQ *COFFEE SHOP": "Local Coffee"
```

### Category Overrides
<!-- Transactions that should be categorized differently than LunchMoney defaults -->
```yaml
category_overrides: []
  # - payee_contains: "SUBSCRIPTION"
  #   should_be: "Software"
```

### Recurring Items Not in LunchMoney
<!-- Manual tracking for items LunchMoney doesn't catch -->
```yaml
manual_recurring: []
  # - name: "Annual domain renewal"
  #   amount: 15.00
  #   cadence: yearly
  #   expected_month: 3
```

---

## Session History

### Decisions Made
<!-- Log of subscription decisions for reference -->

#### Template Entry
```yaml
# - date: YYYY-MM-DD
#   subscription: "Service Name"
#   decision: "keep|cancel|downgrade|watchlist"
#   reason: "Why this decision was made"
#   savings: 0  # Annual savings if cancelled
```

---

## Insights & Notes

### Spending Patterns Noticed
<!-- Observations about spending behavior -->
-

### Seasonal Considerations
<!-- Things to remember about certain times of year -->
- January: Annual subscriptions often renew
- November/December: Holiday shopping increases
- Summer: Travel spending may increase

### Action Items
<!-- Outstanding tasks related to finances -->
- [ ]

---

## Configuration

### Analysis Preferences
```yaml
analysis_config:
  # Default period for spending overview
  default_period: "last_month"  # this_month, last_month, last_3_months, ytd

  # Thresholds for flagging
  unused_subscription_days: 30  # Days without activity to flag as "unused"
  price_increase_threshold: 0.10  # 10% increase triggers alert

  # Report settings
  auto_save_reports: true
  include_transfers_in_totals: false
```
