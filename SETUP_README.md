# Discord Temp Voice Bot Setup

This is a production-ready Discord bot with advanced temp voice channel management, camera enforcement, leaderboards, and more.

## Features

- **Auto Temp Voice Channels**: Join-to-create system with MongoDB persistence
- **Interactive Control Panel**: Button-based UI for channel management
- **Secure Ownership**: Only channel creators can control their channels
- **Slash Commands**: Fallback commands for all features
- **Camera Enforcement**: Automatic muting for users without camera
- **Leaderboards**: Voice and camera activity tracking
- **TODO System**: Daily task management with file attachments
- **Anti-Nuke Protection**: Advanced security features

## Prerequisites

- Python 3.10+
- MongoDB Atlas account (or local MongoDB)
- Discord Bot Token

## Installation

1. **Clone or download the files**
   - `main.py` - Main bot code
   - `requirements.txt` - Python dependencies
   - `.env.example` - Environment configuration template

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in your configuration:
     ```env
     DISCORD_TOKEN=your_bot_token
     CLIENT_ID=your_client_id
     GUILD_ID=your_server_id
     MONGODB_URI=your_mongodb_connection_string
     TEMP_CATEGORY_ID=category_id_for_temp_channels
     INTERFACE_CHANNEL_ID=channel_id_for_control_panel
     LOBBY_CHANNEL_ID=channel_id_to_join_for_creating_temp_vc
     OWNER_ID=your_discord_user_id
     ```

4. **Set up Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to Bot section and create a bot
   - Copy the token to `.env`
   - Enable all Privileged Gateway Intents
   - Add bot to your server with these permissions:
     - Send Messages
     - Use Slash Commands
     - Connect
     - Speak
     - Move Members
     - Manage Channels
     - Manage Roles
     - Timeout Members
     - Ban Members

5. **Configure Channel IDs**
   - Create a category for temp voice channels
   - Create a text channel for the control panel
   - Create a voice channel as the "lobby" (join to create temp VC)
   - Get the IDs and put them in `.env`

6. **MongoDB Setup**
   - Create a MongoDB Atlas cluster or use local MongoDB
   - Create database: `discord_bot`
   - Collection: `tempvoice` (will be created automatically)
   - Whitelist your IP (0.0.0.0/0 for testing)

## Running the Bot

```bash
python main.py
```

The bot will:
- Connect to Discord
- Sync slash commands
- Send the control panel to the interface channel
- Start monitoring voice channels

## Usage

### Temp Voice System

1. **Create Channel**: Join the lobby voice channel
2. **Control Channel**: Use buttons in the interface channel or slash commands
3. **Auto Delete**: Channel deletes when empty

### Control Panel Buttons

- 🔒 **Lock**: Prevent @everyone from connecting
- 🔓 **Unlock**: Allow @everyone to connect
- 👁 **Hide**: Hide channel from @everyone
- 👁‍🗨 **Unhide**: Show channel to @everyone
- 👥 **Limit**: Set user limit (modal input)
- ✏ **Rename**: Rename channel (modal input)
- ✅ **Permit**: Allow specific user
- ❌ **Deny**: Block specific user
- 👑 **Claim**: Claim ownership if original owner left
- 🔄 **Transfer**: Transfer ownership to another user
- 🎧 **Bitrate**: Change audio quality
- 🌍 **Region**: Change voice region

### Slash Commands

All features are available as slash commands:
- `/create` - Create temp channel
- `/delete` - Delete your channel
- `/rename <name>` - Rename channel
- `/limit <number>` - Set user limit
- `/lock` - Lock channel
- `/unlock` - Unlock channel
- `/permit <user>` - Allow user
- `/deny <user>` - Block user

## Database Schema

### tempvoice Collection
```json
{
  "channel_id": 123456789,
  "owner_id": 987654321,
  "guild_id": 111111111,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Security Features

- Owner-only control validation
- Anti-spam protection
- VC hopping detection
- Audit logging
- Trusted user whitelisting
- Anti-nuke channel recovery

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MONGODB_URI format
   - Verify IP whitelist
   - Ensure database user has read/write permissions

2. **Commands Not Appearing**
   - Wait up to 1 hour for global sync
   - Use `/sync` command if owner
   - Check bot permissions

3. **Control Panel Not Working**
   - Ensure INTERFACE_CHANNEL_ID is correct
   - Check bot has message send permissions
   - Verify channel exists

4. **Temp Channels Not Creating**
   - Check LOBBY_CHANNEL_ID
   - Verify TEMP_CATEGORY_ID exists
   - Ensure bot has manage channels permission

### Logs

Check console output for detailed error messages and debug information.

## Deployment

### Railway (Recommended)

1. Connect GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy

### Docker

```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Support

For issues, check the logs and ensure all environment variables are correctly set.