from .gaming import Gaming

cogs = (Gaming,)


def setup(bot):
    for cog in cogs:
        try:
            print(f'loading task extension {cog.__name__}...')
            bot.add_cog(cog(bot))
        except Exception as e:
            print(f'error loading {cog.__name__}: {e}')
    print('task extensions loading finished :)')