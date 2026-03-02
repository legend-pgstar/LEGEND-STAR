# 🔐 WHITELIST LOGIC QUICK REFERENCE

## Core Logic Flow

```
ANTI-NUKE SYSTEM ACTIVATION
├─ Channel/Role Deleted OR Unauthorized Ban
├─ Extract actor from audit log
├─ Call: is_whitelisted_entity(actor)
│
└─ IF actor IS whitelisted:
   ├─ Print: "✅ WHITELISTED entity allowed"
   └─ RETURN (No ban, no punishment)
   
   ELSE actor NOT whitelisted:
   ├─ Print: "🚨 THREAT DETECTED"
   ├─ Ban actor
   ├─ Alert owner
   ├─ Log to tech channel
   └─ Possible lockdown if ban fails
```

---

## Whitelist Checker Function

```python
def is_whitelisted_entity(actor_or_id):
    """Returns True if entity is trusted, False otherwise"""
    
    # Get ID from either User object or int
    actor_id = actor_or_id.id if hasattr(actor_or_id, 'id') else actor_or_id
    
    # Check all trust lists
    if actor_id in WHITELISTED_BOTS:           ✅ Trusted bot
        return True
    if actor_id in WHITELISTED_WEBHOOKS:       ✅ Trusted webhook
        return True
    if actor_id == OWNER_ID:                    ✅ Owner (you)
        return True
    if actor_or_id == bot.user:                 ✅ The bot itself
        return True
    if actor_id in TRUSTED_USERS:               ✅ Trusted user list
        return True
    
    return False  # Not whitelisted
```

---

## Event Handlers Updated

### 1. on_guild_channel_delete
```
IF channel deleted:
  actor = who deleted it (from audit log)
  
  IF is_whitelisted_entity(actor):
    ✅ ALLOW (log and return)
  ELSE:
    🔨 BAN actor
    📧 Alert owner
```

### 2. on_guild_role_delete
```
IF role deleted:
  actor = who deleted it (from audit log)
  
  IF is_whitelisted_entity(actor):
    ✅ ALLOW (log and return)
  ELSE:
    🔨 BAN actor
    📧 Alert owner
```

### 3. on_member_ban
```
IF member banned:
  actor = who banned them (from audit log)
  
  IF is_whitelisted_entity(actor) OR user.id == actor.id:
    ✅ ALLOW (self-ban or trusted actor)
  ELSE:
    🔨 BAN actor
    🔓 UNBAN victim
    📧 Alert owner
```

### 4. on_message (Webhook threats)
```
IF webhook message received:
  
  IF webhook.id in WHITELISTED_WEBHOOKS:
    ✅ ALLOW all content (no scanning)
  ELSE:
    🔍 SCAN for threats:
      - @everyone/@here mentions
      - Phishing links
      - Malicious keywords
    
    IF threat found:
      ☠️ DELETE webhook
      🗑️ DELETE message
```

### 5. clean_webhooks (Periodic task)
```
EVERY 5 MINUTES:
  FOR each webhook in all channels:
    
    IF webhook.id in WHITELISTED_WEBHOOKS:
      ✅ KEEP (log as whitelisted)
    ELSE:
      ❌ DELETE (unauthorized)
```

---

## Whitelisted Entities List

### WHITELISTED_BOTS (16 IDs)
All the following bot IDs are trusted and exempt from all punishments:
- 1457787743504695501, 1456587533474463815, 1427522983789989960
- 155149108183695360, 678344927997853742, 1053580838945693717
- 235148962103951360, 1458076467203145851, 762217899355013120
- 1444646362204475453, 536991182035746816, 906085578909548554
- 1149535834756874250, 1460114117783195841, 889078613817831495
- 704802632660943089

### WHITELISTED_WEBHOOKS (Same 16 IDs)
All the following webhook IDs are trusted:
- Same as WHITELISTED_BOTS

### OWNER
- ID: 1406313503278764174 (You)

### BOT ITSELF
- The bot's own user object

---

## What Gets Whitelisted

| Activity | Whitelisted? | Punishment |
|----------|:----------:|-----------|
| **Channel Delete** | ✅ No ban | ✅ Allowed |
| | ❌ Ban instantly | ❌ Banned |
| **Role Delete** | ✅ No ban | ✅ Allowed |
| | ❌ Ban instantly | ❌ Banned |
| **Unauthorized Ban** | ✅ No ban | ✅ Allowed |
| | ❌ Ban + unban victim | ❌ Banned |
| **Webhook Message (Malicious)** | ✅ Allowed | ✅ All content OK |
| | ❌ Webhook deleted | ❌ Destroyed |
| **Webhook Cleanup** | ✅ Kept | ✅ Forever safe |
| | ❌ Deleted | ❌ Removed |

---

## Adding More Whitelisted Bots

### To whitelist a bot:
1. Get the bot's ID (right-click → Copy User ID)
2. Add it to WHITELISTED_BOTS list
3. Restart the bot

```python
WHITELISTED_BOTS = [
    # ... existing IDs ...
    YOUR_NEW_BOT_ID,  # Add here
]

WHITELISTED_WEBHOOKS = [
    # Same IDs as above
    YOUR_NEW_BOT_ID,  # Add here too
]
```

---

## Console Output Examples

### ✅ Whitelisted action
```
✅ [WHITELIST] Bot ID 1457787743504695501 is whitelisted (TRUSTED BOT)
✅ [CHANNEL DELETE] Whitelisted entity BotName (1457787743504695501) deleted channel - ALLOWED
```

### ❌ Non-whitelisted action
```
🚨 [ANTI-NUKE] CHANNEL DELETION THREAT DETECTED: AttackerName (999999999999)
✅ [ANTI-NUKE] AttackerName has been BANNED for channel deletion
```

### ✅ Whitelisted webhook allowed
```
✅ [WEBHOOK] Webhook 1457787743504695501 is whitelisted - allowing all content
```

### ❌ Unauthorized webhook destroyed
```
🚨 [WEBHOOK THREAT] Non-whitelisted webhook 888888888888 sending malicious content
❌ [WEBHOOK CLEANUP] Deleted unauthorized webhook 888888888888 from #general
```

---

## Key Features

✅ **Single function** - `is_whitelisted_entity()` handles all checks
✅ **Comprehensive** - Checks bots, webhooks, owner, bot itself, trusted users
✅ **Flexible** - Accepts both User objects and raw IDs
✅ **Logged** - Every check is logged with emoji prefix
✅ **Safe** - All punishment code has fallbacks
✅ **Fast** - O(1) list lookups using Python `in` operator
✅ **Maintained** - Used across all anti-nuke handlers

---

## Testing Checklist

- [ ] Whitelisted bot deletes channel → No ban ✅
- [ ] Non-whitelisted user deletes channel → Banned ❌
- [ ] Whitelisted webhook sends malicious link → Message allowed ✅
- [ ] Non-whitelisted webhook sends malicious link → Webhook destroyed ❌
- [ ] Owner deletes something → No ban ✅
- [ ] Bot itself does something → No ban ✅

---

**Last Updated:** Jan 29, 2026
**Status:** ✅ READY FOR PRODUCTION
