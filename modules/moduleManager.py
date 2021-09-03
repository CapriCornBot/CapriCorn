import discord
from discord.ext import commands
import os
from os import path

loadedModules = []


async def loadModules(client):
    client.logger.info(
        "╔════════╦══════════════════════╦══════════╦═════════════════╦════════════════════════════════╦══════════╗"
    )
    client.logger.info(
        f"║ {middle_text('Status', 6)} ║ {middle_text('Name')} ║ {middle_text('Version', 8)} ║ {middle_text('Author', 15)} ║ {middle_text('Beschreibung', 30)} ║ Dev Mode ║"
    )
    client.logger.info(
        "╠════════╬══════════════════════╬══════════╬═════════════════╬════════════════════════════════╬══════════╣"
    )
    moduleCount = 0
    moduleSuccessCount = 0
    moduleFailCount = 0
    filePath = f"{path.dirname(path.abspath(__file__))}{path.sep}"
    for x in [
        c for c in os.listdir(f"{filePath}/") if c not in ["__init__.py", "__pycache__", "moduleManager.py"]
    ]:
        moduleCount = moduleCount + 1
        try:
            x2 = __import__(
                f"modules.{x.replace('.py', '')}.module", globals(), locals(), [x]
            )
            loadedModules.append(x2)
            client.logger.info(
                f"║ {middle_text('✅', 5)} ║ {middle_text(x2.Info.name)} ║ {middle_text(x2.Info.version, 8)} ║ {middle_text(x2.Info.author, 15)} ║ {middle_text(x2.Info.description, 30)}"
                + (
                    f" ║ {middle_text('✅',7)} ║"
                    if hasattr(x2.Info, "dev_mode") and x2.Info.dev_mode == True
                    else f" ║ {middle_text('❌', 7)} ║"
                )
            )
            moduleSuccessCount = moduleSuccessCount + 1
        except Exception as x3:
            client.logger.error(
                f"║ ❌ ║ {middle_text(x2.Info.name)} ║ {middle_text(x2.Info.version, 8)} ║ {middle_text(x2.Info.author, 10)} ║ {middle_text(x2.Info.description, 30)}"
            )
            client.logger.error(x3)
            moduleFailCount = moduleFailCount + 1
    client.logger.info(
        "╠════════╩══════════════════════╩══════════╩═════════════════╩════════════════════════════════╩══════════╣"
    )
    client.logger.info(
        "║ " + middle_text(f"Es wurden {moduleCount} Module geladen!", 102) + " ║"
    )
    client.logger.info(
        "╠═══════════════════════════════════════════════════╦╦═══════════════════════════════════════════════════╣"
    )
    client.logger.info(
        f"╠ "
        + middle_text(f"{moduleSuccessCount} Erfolgreich", 49)
        + " ║║ "
        + middle_text(f"{moduleFailCount} Fehlerhaft", 49)
        + " ║"
    )
    client.logger.info(
        "╚═══════════════════════════════════════════════════╩╩═══════════════════════════════════════════════════╝"
    )
    client.logger.info("Module werden gestartet")
    for m in loadedModules:
        try:
            await m.Module().on_load(client=client)
        except Exception as ex:
            client.logger.error(f"❌ {m.Info.name} ║ {ex}")

    client.logger.info("Alle Module gestartet!")
    client.dispatch("modules_loaded")


def middle_text(txt, max_s=20):
    return txt + " " * (max_s - len(txt))
