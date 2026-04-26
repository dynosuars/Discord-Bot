import discord

class message:
    def __init__(self, message: discord.message.Message):
        self.content = message.content
        self.author = message.author
        self.channel = message.channel
        self.author_id = message.author.id

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

    def __eq__(self, other):
        return self.content == other.content

    def __hash__(self):
        return hash(self.content)

    def __add__(self, other):
        return self.content + other.content


