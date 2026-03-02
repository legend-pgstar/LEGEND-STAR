# MongoDB Atlas SSL/TLS Connection Troubleshooting

## Issue: SSL Handshake Failed
The bot is failing to connect to MongoDB Atlas with SSL errors:
```
SSL handshake failed: [SSL: TLSV1_ALERT_INTERNAL_E...]
```

## Root Causes
1. **IP Whitelist Issue** - Your current IP is not whitelisted in MongoDB Atlas
2. **Docker Environment** - If running in Docker, `localhost` connections won't work
3. **SSL/TLS Version Mismatch** - Certificate validation issues
4. **Network Firewall** - ISP or corporate firewall blocking MongoDB ports

## Solutions (Try in Order)

### Solution 1: Update MongoDB Atlas IP Whitelist
1. Go to https://cloud.mongodb.com
2. Login to your MongoDB Atlas account
3. Click "Network Access" in the left sidebar
4. Click "Add IP Address"
5. **Option A (If testing locally):** Add your current public IP
   - You can find it at https://whatismyipaddress.com
6. **Option B (If using Docker):** Add `0.0.0.0/0` (allows all IPs - development only!)
7. Click "Confirm"
8. Wait 2-3 minutes for changes to apply
9. Restart the bot

### Solution 2: Verify MongoDB Credentials
Check your `.env` file:
```dotenv
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.jtwsmus.mongodb.net/legend_star?retryWrites=true&w=majority
```

Ensure:
- ✅ Username is correct (case-sensitive)
- ✅ Password is correct (URL-encode special characters like `@` as `%40`)
- ✅ Cluster name is correct (`cluster0.jtwsmus...`)
- ✅ Database name is correct (`legend_star`)

### Solution 3: Check Cluster Status
1. Go to MongoDB Atlas Dashboard
2. Click your cluster ("Cluster0")
3. Check if the cluster is running (green status)
4. If paused, click "Resume"

### Solution 4: Create New Database User (If Stuck)
1. In MongoDB Atlas, go to "Database Access"
2. Click "Add New Database User"
3. Create a new user with a simple password (no special chars)
4. Update `MONGODB_URI` in `.env` with the new credentials
5. Restart the bot

## Updated Connection Strategies

The bot now uses 4 improved connection strategies:

1. **Custom SSL Context** - Uses Python SSL with relaxed validation
2. **Relaxed TLS without Retry Writes** - May help with Atlas stability
3. **Direct Connection** - Bypasses SRV lookup (slower but more stable)
4. **Extended Timeout** - Longer wait for slow networks

If all fail, the bot runs with **in-memory cache** (data lost on restart).

## Docker-Specific Fixes

If running in Docker:

### Option 1: Add to IP Whitelist
```
Whitelist: 0.0.0.0/0
```

### Option 2: Use Environment Variables
```dockerfile
ENV MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
```

### Option 3: Network Mode
Ensure Docker container can reach external networks:
```bash
docker run --network host mybot:latest
```

## Testing the Connection

1. Test with Python directly:
```bash
python -c "from pymongo import MongoClient; c = MongoClient('mongodb+srv://...'); c.admin.command('ping'); print('Connected!')"
```

2. Check MongoDB Atlas logs:
   - Go to Monitoring → Logs
   - Look for connection attempts

## Still Not Working?

1. **Check firewall:** Try disabling antivirus/firewall temporarily
2. **Use different network:** Try with mobile hotspot instead of home WiFi
3. **Contact MongoDB Support:** Open a ticket at mongodb.com/support
4. **Alternative:** Use MongoDB Community Server (local installation)

## Fallback: Run Bot Without MongoDB

The bot currently works without MongoDB (in-memory only). To enable:
- All data will be lost on restart
- Leaderboards reset each session
- TODOs don't persist

For production, MongoDB is required for data persistence.
