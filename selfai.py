import discord
from discord.ext import commands, tasks
import logging
import asyncio
import openai
import random

client = commands.Bot(command_prefix = '!', self_bot=True)

DISCORD_TOKEN = "discord-user-token"
OPENAI_API_KEY = "openai-api-key"


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


openai.api_key = OPENAI_API_KEY


conversation_history = {}
ai_enabled = True
message_cache = {}
MESSAGE_CACHE_INTERVAL = 5

class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f'By netnsher :3 / Logged in as {self.user} (ID: {self.user.id})')
        logger.info('Created by netnsher :3')
        await self.change_presence(activity=discord.Game(name="AI Assistant"))
        self.message_cache_check.start()

    @tasks.loop(seconds=MESSAGE_CACHE_INTERVAL)
    async def message_cache_check(self):
        for user_id in list(message_cache.keys()):
            data = message_cache[user_id]
            if data['messages']:
                combined_message = " ".join(data['messages'])
                await self.handle_ai_response(data['message'], combined_message)
                data['messages'] = []

    async def on_message(self, message):
        logger.debug(f'Message received: {message.content}')

        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            if message.content.startswith('!toggle_ai'):
                logger.info('Toggle AI command triggered.')
                await self.toggle_ai(message)
            else:
                logger.info('Handling AI response.')
                await self.cache_message(message)

    async def cache_message(self, message):
        user_id = message.author.id
        if user_id not in message_cache:
            message_cache[user_id] = {'messages': [], 'message': message}
        message_cache[user_id]['messages'].append(message.content)
        logger.debug(f'Cached message for user {user_id}: {message.content}')

    async def toggle_ai(self, message):
        global ai_enabled
        ai_enabled = not ai_enabled
        status = "enabled" if ai_enabled else "disabled"
        await message.channel.send(f"AI responses are now {status}")
        logger.debug(f'AI responses toggled: {status}')

    async def handle_ai_response(self, message, combined_message=None):
        logger.debug(f'Handling AI response for user: {message.author}')
        if not ai_enabled:
            return

        query = combined_message if combined_message else message.content
        base_prompt = (
            "This is your base prompt: DESCRIBE ITS PURPOSE "
            "now for how you speak: DESCRIBE HOW IT SHOULD TYPE "
            "your personality: DESCRIBE THE BOTS PERSONALITY"
            f"{query}")

        async with message.channel.typing():
            await asyncio.sleep(2)
            user_id = message.author.id
            history = self.get_conversation(user_id)
            prompt_with_history = "".join(history + [base_prompt])

            try:
                response = openai.chat.completions.create(
                    model="gpt-4",  # ADJUST MODEL AS NEEDED ex: gpt-3.5 / gpt-4 / gpt-4o
                    messages=[{"role": "user", "content": prompt_with_history}]
                )

                response_text = response.choices[0].message.content # Extract response text

                self.add_to_conversation(user_id, query)
                self.add_to_conversation(user_id, response_text)

                # 20% chance to split response for more realistic responses
                if random.random() < 0.2:
                    halfway_point = len(response_text) // 2
                    part1 = response_text[:halfway_point].strip()
                    part2 = response_text[halfway_point:].strip()

                    await self.send_message_in_chunks(message, part1)
                    await self.send_message_in_chunks(message, part2)
                else:
                    await self.send_message_in_chunks(message, response_text)

                logger.info(f'Sent AI response to {message.author}: {response_text}')
            except Exception as e:
                logger.error(f"Error interacting with OpenAI API: {str(e)}")
                await message.channel.send(f"Error interacting with OpenAI API: {str(e)}")
                logger.info(f'Error sent to {message.author}')

    def add_to_conversation(self, user_id, message):
        logger.debug(f'Adding message to conversation history for user: {user_id}')
        if user_id in conversation_history:
            conversation_history[user_id].append(message)
        else:
            conversation_history[user_id] = [message]

    def get_conversation(self, user_id):
        logger.debug(f'Retrieving conversation history for user: {user_id}')
        return conversation_history.get(user_id, [])

    async def send_message_in_chunks(self, message, content):
        logger.debug(f'Sending message in chunks to channel: {message.channel.name if isinstance(message.channel, discord.TextChannel) else "Direct Message"}')
        max_chunk_size = 1900
        chunks = [content[i:i + max_chunk_size] for i in range(0, len(content), max_chunk_size)]
        for chunk in chunks:
            await message.channel.send(chunk)
            logger.debug(f'Sent chunk to {message.channel.name if isinstance(message.channel, discord.TextChannel) else "Direct Message"}: {chunk}')

logger.info('Starting bot...')
client = MyClient()
client.run(DISCORD_TOKEN)

