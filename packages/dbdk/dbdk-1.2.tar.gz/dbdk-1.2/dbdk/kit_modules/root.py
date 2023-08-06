import discord
from typing import Tuple, Awaitable, Union
from collections import namedtuple

from .embed import EmbedList
from .view import View


RootItems = namedtuple("RootItems", ["embeds", "view"])
# class RootItems(TypedDict):
#     embeds: discord.Embed = None
#     view: discord.ui.View = None


class Root:
    def __init__(
        self,
        respondable: Union[discord.Message, discord.Interaction],
        ctx: discord.ApplicationContext = None,
    ):
        self.origin = respondable
        self.ctx = ctx

        self.__set_edit_func()

        # set root items
        self.view : View = None
        self.embeds : EmbedList = None
        
        # use to remove the starting content from the message when it loads
        self.__loaded: bool = False

    @property
    def items(self) -> Tuple[EmbedList | None, View | None]:
        """Returns A tuple containing root items"""
        return (self.embeds, self.view)
        
    def __set_edit_func(self) -> None:
        self.__edit_func = (
            self.origin.edit_original_response 
            if isinstance(self.origin, discord.Interaction) 
            else self.origin.edit
        )

    def _set_root_items(self, items: RootItems) -> None:
        self._items = items

        for key in items._fields:
            self.__setattr__(
                key,
                self._items.__getattribute__(key),
            )

    def __iter__(self):
        return self._items.__iter__()

    def __next__(self):
        return self._items.__next__()

    async def edit(self, **kwargs) -> Awaitable[None]:
        """
        `content: str = None`,
        `embed: discord.Embed = None`,
        `embeds: List[discord.Embed ] = None`,
        `file: Sequence[discord.File] = None`,
        `files: List[Sequence[discord.File]] = None`,
        `attachments: List[discord.Attachment] = None`,
        `suppress: bool = False`,
        `delete_after: int = None`,
        `allowed_mentions: discord.AllowedMentions = None`,
        `view: discord.ui.View = None`
        """

        if not self.__loaded:
            # remove starting content
            if not kwargs.get("content"):
                kwargs["content"] = ""

            self.__loaded = True

        await self.__edit_func(**kwargs)


    # NOT DONE YET
    async def relocate(self, respondable: Union[discord.Message,discord.Interaction], ctx: discord.ApplicationContext = None) -> None:
        if respondable == self.origin:
            return

        # deleted old origin
        try:
            if isinstance(self.origin, discord.Message):
                await self.origin.delete()

            elif isinstance(self.origin, discord.Interaction):
                await self.origin.delete_original_response()

        except:
            await self.edit(
                content="`[Deleted]`",
                embeds=[],
                view=None
            )

        # set new origin
        self.origin = respondable
        self.ctx = ctx or self.ctx

        self.__set_edit_func()

        # set up origin
        await self.edit(
            embeds=self.embeds,
            view=self.view
        )
