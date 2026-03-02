import datetime

KOLKATA = None  # Keep placeholder; main defines timezone if needed


def format_time(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m"


def get_medal_emoji(position: int) -> str:
    # 1 -> ????, 2 -> ??, 3 -> ??, 4-10 -> ???, 11+ -> ??
    if position == 1:
        return "\U0001F48E\U0001F451"
    if position == 2:
        return "\U0001F948"
    if position == 3:
        return "\U0001F949"
    if 4 <= position <= 10:
        return "\U0001F396\uFE0F"
    return "\U0001F3AF"


def generate_leaderboard_text(cam_on_list, cam_off_list):
    """Render the /lb message (top 5) like the provided screenshot."""
    try:
        from zoneinfo import ZoneInfo
        now_dt = datetime.datetime.now(ZoneInfo('Asia/Kolkata'))
    except Exception:
        now_dt = datetime.datetime.now()

    now = now_dt.strftime('%d %b %Y | %I:%M %p')

    # Only show users who actually studied today (mins > 0).
    cam_on_filtered = [(n, m) for n, m in cam_on_list if (m or 0) > 0]
    cam_off_filtered = [(n, m) for n, m in cam_off_list if (m or 0) > 0]

    border_top = '\u2554' + ('\u2550' * 54) + '\u2557'
    border_bot = '\u255a' + ('\u2550' * 54) + '\u255d'
    rule = '\u2501' * 54

    trophy = '\U0001F3C6'
    moon = '\U0001F319'
    clock = '\u23F0'
    cam_on_icon = '\U0001F4F9'  # video camera
    cam_off_icon = '\U0001F4F4'  # cam off

    em_dash = '\u2014'
    stopwatch = '\u23F1\uFE0F'

    text = (
        f"{border_top}\n"
        f"        {trophy} LEGEND STAR {trophy}\n"
        f"     {moon} Daily Leaderboard Champion {moon}\n"
        f"        {clock} {now} IST\n"
        f"{border_bot}\n\n"
        f"{cam_on_icon} **CAM ON {em_dash} TOP 5**\n"
        f"{rule}\n"
    )

    if cam_on_filtered:
        for i, (name, mins) in enumerate(cam_on_filtered[:5], 1):
            medal = get_medal_emoji(i)
            text += f"{medal}  #{i} **{name}** {em_dash} {stopwatch} {format_time(int(mins))}\n"
    else:
        text += '\U0001F4DA *No data yet. Start studying!*\n'

    text += f"\n{rule}\n"
    text += f"{cam_off_icon} **CAM OFF {em_dash} TOP 5**\n"
    text += f"{rule}\n"

    if cam_off_filtered:
        for i, (name, mins) in enumerate(cam_off_filtered[:5], 1):
            medal = get_medal_emoji(i)
            text += f"{medal}  #{i} **{name}** {em_dash} {stopwatch} {format_time(int(mins))}\n"
    else:
        text += '\U0001F910 *No silent sessions yet.*\n'

    text += (
        f"\n{rule}\n"
        '\u2728 Auto Generated at **11:55 PM**\n'
        '\U0001F504 Daily Reset at **11:59 PM**\n'
        '\U0001F525 Keep Grinding Legends!'
    )
    return text


def user_rank(username: str, cam_on_data, cam_off_data):
    # sort descending by minutes
    cam_on_sorted = sorted(cam_on_data, key=lambda x: x[1], reverse=True)
    cam_off_sorted = sorted(cam_off_data, key=lambda x: x[1], reverse=True)

    result = []
    result.append("╔══════════════════════╗")
    result.append("      🏆 YOUR RANK 🏆")
    result.append("╚══════════════════════╝")
    result.append(f"👤 User: {username}")
    result.append("━━━━━━━━━━━━━━━━━━━━━━")

    # CAM ON
    cam_on_users = [u[0] for u in cam_on_sorted]
    if username in cam_on_users:
        rank = cam_on_users.index(username) + 1
        mins = cam_on_sorted[rank - 1][1]
        medal = get_medal_emoji(rank)
        result.append("🎥 CAM ON")
        result.append(f"{medal} Rank: #{rank} / {len(cam_on_sorted)}")
        result.append(f"⏱ Time: {format_time(mins)}")
        result.append("")
    else:
        result.append("🎥 CAM ON")
        result.append("❌ Not active today")
        result.append("")

    # CAM OFF
    cam_off_users = [u[0] for u in cam_off_sorted]
    if username in cam_off_users:
        rank = cam_off_users.index(username) + 1
        mins = cam_off_sorted[rank - 1][1]
        medal = get_medal_emoji(rank)
        result.append("📴 CAM OFF")
        result.append(f"{medal} Rank: #{rank} / {len(cam_off_sorted)}")
        result.append(f"⏱ Time: {format_time(mins)}")
    else:
        result.append("📴 CAM OFF")
        result.append("❌ Not active today")

    result.append("")
    result.append("🔥 Keep pushing. Legends rise daily!")
    return "\n".join(result)
