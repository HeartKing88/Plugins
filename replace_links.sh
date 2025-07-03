#!/bin/bash

# ------------------------
# ?? MULTI LINK REPLACER
# ------------------------

# Replace old Telegram link
find . -type f -name "*.py" -exec sed -i 's|https://t.me/II_CHAT_HUB_II|https://t.me/PBX_CHAT|g' {} +

# Replace @mention
find . -type f -name "*.py" -exec sed -i 's|@ll_THE_BAD_BOT_ll|@PBX_CHAT|g' {} +

# You can add more replacements like this:
# find . -type f -name "*.py" -exec sed -i 's|OLD|NEW|g' {} +

# ------------------------
# ?? PUSH TO GITHUB
# ------------------------
git add .
git commit -m "?? Replaced old TG links with @PBX_CHAT and https://t.me/PBX_CHAT"
git push

echo "✅ All links replaced and changes pushed to GitHub!"
