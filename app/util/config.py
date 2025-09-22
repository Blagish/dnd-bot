import os

class Config:
    ai_base_url = ''
    use_ai_talking = False
    beta_test = False
    discord_id = os.environ.get("DISCORD_TOKEN")
    use_karmic = False
    karmic_dice = [20]
    kappa = 0.35



config = Config()
