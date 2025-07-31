from pyrogram import Client
from pyrogram.types import Message

from . import Config, HelpMenu, db, Pbxbot, on_message

@on_message("stan", allow_stan=True)
async def stanUsers(client: Client, message: Message):
    Pbx = await Pbxbot.edit(message, "__Fetching users...__")

    users = await db.get_stans(client.me.id)
    if not users:
        return await Pbxbot.delete(Pbx, "__No stans found!__")

    text = f"**Total stans:** `{len(users)}`\n\n"
    for user in users:
        try:
            user = await client.get_users(user["user_id"])
            mention = user.mention
            userid = user.id
        except Exception:
            userid = user["user_id"]
            mention = "Unknown Peer"
        text += f"• {mention} (`{userid}`)\n"

    await Pbx.edit(text)

@on_message("addsudo", allow_stan=False)
async def addstan(client: Client, message: Message):
    if len(message.command) < 2:
        if not message.reply_to_message:
            return await Pbxbot.delete(
                message,
                "__Reply to a user or give me a user id to add them as a stan!__",
            )
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(
                message, "__Give me a valid user id to add them as a stan!__"
            )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "__I can't be a stan of myself!__")

    if user.id in Config.PERMANENT_STAN:
        return await Pbxbot.delete(message, "__This user is a permanent stan!__")

    if await db.is_stan(client.me.id, user.id):
        return await Pbxbot.delete(message, "__This user is already a stan!__")

    await db.add_stan(client.me.id, user.id)
    if user.id not in Config.STAN_USERS:
        Config.STAN_USERS.append(user.id)
    await Pbxbot.delete(message, f"__Added {user.mention} as a stan!__")

@on_message("rmsudo", allow_stan=False)
async def delstan(client: Client, message: Message):
    if len(message.command) < 2:
        if not message.reply_to_message:
            return await Pbxbot.delete(
                message,
                "__Reply to a user or give me a user id to remove them from stans!__",
            )
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(
                message, "__Give me a valid user id to remove them from stans!__"
            )

    if user.id in Config.PERMANENT_STAN:
        return await Pbxbot.delete(message, "__Cannot remove a permanent stan!__")

    if await db.is_stan(client.me.id, user.id):
        await db.rm_stan(client.me.id, user.id)
        if user.id in Config.STAN_USERS:
            Config.STAN_USERS.remove(user.id)
        await Pbxbot.delete(message, f"__Removed {user.mention} from stans!__")
    else:
        await Pbxbot.delete(message, "__This user is not a stan!__")

@on_message("superaddsudo", allow_stan=False)
async def add_super_sudo(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await Pbxbot.delete(message, "__Only the owner can add super sudo users!__")

    if len(message.command) < 2:
        if not message.reply_to_message:
            return await Pbxbot.delete(
                message,
                "__Reply to a user or give me a user id to add them as a super sudo!__",
            )
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(
                message, "__Give me a valid user id to add them as a super sudo!__"
            )

    if user.id == client.me.id:
        return await Pbxbot.delete(message, "__I can't be a super sudo of myself!__")

    if user.id in Config.PERMANENT_STAN:
        return await Pbxbot.delete(message, "__This user is already a super sudo!__")

    if await db.is_stan(client.me.id, user.id):
        await db.rm_stan(client.me.id, user.id)
        if user.id in Config.STAN_USERS:
            Config.STAN_USERS.remove(user.id)

    Config.PERMANENT_STAN.append(user.id)
    await Pbxbot.delete(message, f"__Added {user.mention} as a super sudo!__")

@on_message("supersudorm", allow_stan=False)
async def remove_super_sudo(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await Pbxbot.delete(message, "__Only the owner can remove super sudo users!__")

    if len(message.command) < 2:
        if not message.reply_to_message:
            return await Pbxbot.delete(
                message,
                "__Reply to a user or give me a user id to remove them from super sudo!__",
            )
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await Pbxbot.delete(
                message, "__Give me a valid user id to remove them from super sudo!__"
            )

    if user.id not in Config.PERMANENT_STAN:
        return await Pbxbot.delete(message, "__This user is not a super sudo!__")

    Config.PERMANENT_STAN.remove(user.id)
    await Pbxbot.delete(message, f"__Removed {user.mention} from super sudo!__")

@on_message("superstans", allow_stan=False)
async def super_stans(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await Pbxbot.delete(message, "__Only the owner can view super sudo users!__")

    Pbx = await Pbxbot.edit(message, "__Fetching super sudo users...__")

    if not Config.PERMANENT_STAN:
        return await Pbxbot.delete(Pbx, "__No super sudo users found!__")

    text = f"**Total super sudo users:** `{len(Config.PERMANENT_STAN)}`\n\n"
    for user_id in Config.PERMANENT_STAN:
        try:
            user = await client.get_users(user_id)
            mention = user.mention
            userid = user.id
        except Exception:
            userid = user_id
            mention = "Unknown Peer"
        text += f"• {mention} (`{userid}`)\n"

    await Pbx.edit(text)

HelpMenu("sudo").add(
    "stan",
    None,
    "Get a list of stan(sudo) users for your client.",
    "stan",
    "A stan(sudo) user can access some of the commands of your client."
).add(
    "addsudo",
    "<reply/username/userid>",
    "Add a stan(sudo) user in your client.",
    "addstan",
    "Be careful while adding a stan user."
).add(
    "rmsudo",
    "<reply/username/userid>",
    "Remove a stan(sudo) user from your client.",
    "delstan"
).add(
    "superaddsudo",
    "<reply/username/userid>",
    "Add a super sudo user (controls all clients). Only for owner.",
    "superaddsudo",
    "Be careful while adding a super sudo user."
).add(
    "supersudorm",
    "<reply/username/userid>",
    "Remove a super sudo user. Only for owner.",
    "supersudorm"
).add(
    "superstans",
    None,
    "Get a list of super sudo users. Only for owner.",
    "superstans"
).info(
    "Stan(sudo) Users"
).done()