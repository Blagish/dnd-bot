from discord.ext import commands
from random import choice, randint
import os
import json


class Talking(commands.Cog, name='Общение со мной :)'):
    def __init__(self, bot):
        self.bot = bot
        self.danika_react = ['а?', 'я тут!', 'меня звали?', 'что-то нужно?', 'чем могу помочь??',
                             'ты чо сука ты чо', 'опять я??', 'каджит ничего не крал', 'доброе утро', 'добрый день', 'добрый вечер'
                             'а? что??', 'аниме', 'гейминг', '*кусь*', 'апчхи', 'без комментариев']
        self.bot_id = os.environ.get('DISCORD_ID')
        self.yes_or_no = ['Ага', 'Неа']
        self.funny_words = ['пизда :)', 'пизда', 'пизда!', 'сковорода']
        whitelist = os.environ.get("TALKING_WHITELIST")
        self.whitelist = json.loads(whitelist)

    def random_danika_reaction(self):
        s = choice(self.danika_react)
        if randint(1, 3) == 1:
            s = s.capitalize()
        return s

    @commands.Cog.listener('on_message')
    async def respond_to_her_name(self, message):
        if message.author == self.bot.user:
            return None
        ctx = message.channel
        print(message.content)
        text = message.content.lower()
        if self.bot_id in text:
            await ctx.send(self.random_danika_reaction())
        elif 'даник' in text:
            if '?' in text:
                await ctx.send(self.funny_response(text))
            elif randint(1, 7) == 1:
                await ctx.send(self.random_danika_reaction())

    @commands.Cog.listener('on_message')
    async def react(self, message):  # beta-test
        if message.guild is not None and message.guild.id not in self.whitelist['react']:
            return None
        REACT_P = 13
        mood_indicators = {'anger': ['блять', 'пиздец', 'ебаный', "какого", "какова", "кусок", "жопа", "аааааааа"],
                           'funney': ["сука", "ору", "кричу", "ахах", "лмао"],
                           'please': ["пожалуйста", "умоляю", "прошу", "ради бога", "пж"]}
        mood_responses = {
            'anger': ['ору', "лошара", "чел ты", "ехехеххехеех", "ухухухухухх", "ыхыхыхыхыхыхы", "поплачь ещё",
                      "они действительно этого заслужили", "обломись"],
            'funney': ["сука", "ору", "кричу", "лмао", "не смешно", "чо шутник типа??"],
            'please': ["окей", "ладно", "так уж и быть", "а ты не лопнешь деточка?", "а по губе", "нет", "не заслужил",
                       "я подумаю", "иди нахуй"]
        }

        if message.author == self.bot.user:
            return None
        ctx = message.channel
        text = message.content.lower()
        vibes = []
        for vibe, signs in mood_indicators.items():
            for sign in signs:
                if sign in text:
                    vibes.append(vibe)
        response = ''
        for vibe in vibes:
            if randint(0, 100) > REACT_P:
                continue
            response = choice(mood_responses[vibe])
        normal_human_emotions = ['OwO', 'uwu', '>w<', ':D', 'D:', ':gun:', 'o_o', 'e_e', 'o.o', ':0', ':>', ':<', '>:<',
                                 ':}', '>:}', '>:]', ':P', '>:P', '(* ^ ω ^)', '(°▽°)', '(◕‿◕)', '(´• ω •`)', '(⌒_⌒;)',
                                 '(・`ω´・)', '(; ･`д･´)', 'ヽ(°〇°)ﾉ']
        if len(response) > 0:
            await ctx.send(response + ' ' + choice(normal_human_emotions))

    def funny_response(self, text):
        if text.replace(' ', '')[-3:] == 'да?':
            return choice(self.funny_words)
        elif text[:2] == 'да' and text.replace(' ', '')[-7:] == 'даника?':
            return choice(self.funny_words).replace('да', 'даника')
        else:
            return choice(self.yes_or_no)

    @commands.command(name='привет', aliases=['hello', 'hewwo', 'owo'])
    async def hello(self, ctx):
        """Привет :)"""
        res = choice(['Привет!', 'Привет :)', 'Hewwo', ' Hewwo :)', 'Привееееет :)'])
        await ctx.send(res)

    @commands.command(name='куку', hidden=True)
    async def kuku(self, ctx):
        """Ку ку?"""
        await ctx.send('быбы')

    @commands.command(name='спасибо', aliases=['спс', 'thanks', 'thx'])
    async def thanks(self, ctx):
        """Поблагодарить меня :)"""
        res = choice(['Пожалуйста!', 'Рада помочь!', 'Всегда пожалуйста', 'Стараюсь :)'])
        await ctx.send(res)

    @commands.command(name='слышь', aliases=['слыш', 'э', 'слiш', 'bruh', 'брух'])
    async def anger(self, ctx):
        """Быкануть на меня :("""
        res = choice(['Виноваты кубики', 'Оно само', 'Это не я', 'Я честно не виновата', 'Все вопросы к кубам!', 'ахах',
                      'лошара', 'меня заставили'])
        await ctx.send(res)
