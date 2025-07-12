import openai
from app.util.config import config
from loguru import logger


class Connection:
    model = 'gemma-2-ataraxy-9b'

    def __init__(self, prompt, model=None):
        self.role = prompt
        with open(f'app/ai_client/prompts/{prompt}.txt', 'r', encoding='utf-8') as file:
            self.prompt = file.read()
            self.system = {'role': 'system', 'content': self.prompt}



class ConnectionManager:
    def __init__(self):
        self.ai_client = openai.Client(base_url=config.ai_base_url, api_key='test')

        self.connections = {'talk': Connection('talk'), 'secretary': Connection('secretary')}


    def send_with_history(self, mode: str, history: list):
        conn = self.connections.get(mode, self.connections['talk'])
        if conn.role != 'talk':
            history.insert(0, conn.system)
        try:
            res = self.ai_client.chat.completions.create(model=conn.model, messages=history)
            msg = res.choices[0].message.content.strip()
            return msg

        except openai.APIConnectionError as e:
            logger.error(e)
            return 'отсутствует подключение к серверу ии'

        except Exception as e:
            logger.error(e)
            return


    def send_prompt(self, mode: str, prompt: str):
        history = [{'role':'user', 'content':prompt}]
        return self.send_with_history(mode, history)

