from discord.ext import commands
from discord import app_commands, Message
from queue import Queue
from app.util.config import config
from app.ai_client.connection_manager import ConnectionManager

import json
import loguru

from app.commands.base import BaseCog

logger = loguru.logger


class AiTalking(BaseCog, name="Общение через нейронку",):
    def __init__(self, bot):
        super().__init__(bot)
        self.manager = ConnectionManager()
        logger.info('loaded AI client')
        self.bot_id = config.discord_id
        self.pikmin = '<:pikmin:1276865893460086864>'
        self.MEMORY_LIMIT = 6
        self.histories = dict()

    async def check_for_commands(self, ctx:commands.Context, prompt: str) -> bool:
        try:
            msg = self.manager.send_prompt('secretary', prompt)
            if msg is None:
                return False
            if '```' in msg:
                msg = msg[8:-4]
            if msg.startswith('null'):
                return False
            msg = json.loads(msg)
            logger.info(msg)
            command = self.bot.get_command(msg.get('command'))
            print('invoking')
            match command.name:
                case 'pf2':
                    await ctx.invoke(command, msg.get('args'), None)
                case 'roll':
                    await ctx.invoke(command, msg.get('args'))
                case 'help':
                    await ctx.invoke(command)
                case 'card52':
                    await ctx.invoke(command)
                case _:
                    print(f'not found {command}')
                    return False
            print('invoked')
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def send_prompt(self, history: Queue) -> str:
        try:
            #print(list(history.queue))
            #msg = self.manager.send_with_history('talk', list(history.queue))
            msg = self.manager.send_prompt('talk', history)
            if msg is None:
                raise ValueError('broke')
            parsed_msg = msg.strip().replace('  ', ' ').replace('[PIKMIN]', self.pikmin)
            #history.put({'role': 'assistant', 'content': parsed_msg})
            return parsed_msg
        except Exception as e:
            logger.error(e)
            return 'я сломалась'

    async def talk(self, ctx: commands.Context, text: str):
        is_command = await self.check_for_commands(ctx, text)
        if is_command:
            return
        await ctx.typing()
        #chat_history = self.histories.get(ctx.channel.id)
        response = await self.send_prompt(text)#chat_history)
        try:
            await ctx.reply(response)
        except Exception as e:
            self.foreseen_error_message(str(e))


    @commands.Cog.listener("on_message")
    async def respond_to_her_name(self, message: Message):
        if message.author == self.bot.user:
            return None
        ctx = await self.bot.get_context(message)

        reply_from_her = False
        if message.reference:
            reply_id = message.reference.cached_message
            if reply_id:
                reply_from_her = reply_id.author == self.bot.user

        text = message.content.replace(self.pikmin, '[PIKMIN]')
        message_h = {'role': 'user', 'content': text}
        chat_history = [message_h] #self.histories.setdefault(ctx.channel.id, Queue(maxsize=self.MEMORY_LIMIT))
        # chat_history.put(message_h)
        logger.debug(f"[MESSAGE] {message.author.name}: {message.content}")
        if 'даник' in text.lower() or self.bot_id in text or reply_from_her:
            await self.talk(ctx, text)


    @commands.hybrid_command(name="talk")
    @app_commands.describe(text="Промпт для Даники без истории (beta)")
    async def hello(self, ctx: commands.Context, text: str):
        """Привет :)"""
        text = text.replace(self.pikmin, '[PIKMIN]')
        message_h = {'role': 'user', 'content': text}
        #chat_history = self.histories.setdefault(ctx.channel.id, Queue(maxsize=8))
        #chat_history.put(message_h)
        await self.talk(ctx, text)
