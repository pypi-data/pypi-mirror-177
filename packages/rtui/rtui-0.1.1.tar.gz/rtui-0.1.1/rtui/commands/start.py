"""Command to trigger the virtual start button."""
from typing import List

from .command import BaseCommand


class StartTriggerCommand(BaseCommand):
    """Trigger the start button."""

    description = "Trigger the virtual start button."

    async def exec(self, args: List[str]) -> None:
        """Execute the command."""
        await self._tui.astoria.trigger_start()
