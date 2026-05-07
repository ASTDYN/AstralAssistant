import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]
DATABASE_URL: str = os.environ["DATABASE_URL"]
DATABASE_USERNAME: str = os.environ["DATABASE_USERNAME"]
DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]

TIMEZONES: list[tuple[str, str]] = [
    ("UTC", "UTC"),
    ("US/Eastern (EST/EDT)", "America/New_York"),
    ("US/Central (CST/CDT)", "America/Chicago"),
    ("US/Mountain (MST/MDT)", "America/Denver"),
    ("US/Pacific (PST/PDT)", "America/Los_Angeles"),
    ("US/Alaska (AKST/AKDT)", "America/Anchorage"),
    ("US/Hawaii (HST)", "America/Honolulu"),
    ("Brazil (BRT/BRST)", "America/Sao_Paulo"),
    ("UK (GMT/BST)", "Europe/London"),
    ("Western Europe (CET/CEST)", "Europe/Paris"),
    ("Central Europe (CET/CEST)", "Europe/Berlin"),
    ("Eastern Europe (EET/EEST)", "Europe/Bucharest"),
    ("Russia (MSK)", "Europe/Moscow"),
    ("Gulf (GST)", "Asia/Dubai"),
    ("India (IST)", "Asia/Kolkata"),
    ("Singapore (SGT)", "Asia/Singapore"),
    ("China (CST)", "Asia/Shanghai"),
    ("Japan (JST)", "Asia/Tokyo"),
    ("Australia/Sydney (AEDT/AEST)", "Australia/Sydney"),
    ("Australia/Perth (AWST)", "Australia/Perth"),
    ("New Zealand (NZDT/NZST)", "Pacific/Auckland"),
]

GAMEPLAY_STYLES: list[str] = [
    "Mining",
    "Logistics",
    "Security",
    "RRRR Services",
]

ROLE_NAMES: dict[str, str] = {
    "unverified": "SC-Unverified",
    "verified": "SC-Verified",
    "officer": "Officer",
    "rank1": "Rank1",
}
