from typing import Any, Sequence, Set
import emoji
import asyncio
import tempfile
from discord import Message, Client
import os
import docker
from logging import Logger
import logging

import re
import os.path
from discord_repl.bot import MessageHandler
from dataclasses import dataclass, field
from discord_repl.executor.docker_executor import DockerExecutor


executors = (
    DockerExecutor({'python'}, 'python', 'python {}', 'script.py'),
    DockerExecutor({'java'}, 'openjdk', 'java {}', 'Script.java'),
    DockerExecutor({'js','javascript'}, 'node:lts', 'node {}', 'script.js'),
    DockerExecutor({'ts','typescript'}, 'lukechannings/deno', 'deno run -q {}', 'script.ts'),
    DockerExecutor({'php'}, 'php:cli', 'php {}', 'script.php'),
    DockerExecutor({'c'}, 'gcc', '/bin/bash -c "gcc {} -o /tmp/a.out;/tmp/a.out"', 'script.c'),
    DockerExecutor({'cpp', 'c++'}, 'gcc', '/bin/bash -c "gcc -x c++ {} -lstdc++ -o /tmp/a.out;/tmp/a.out"', 'script.cpp'),
    DockerExecutor({'rust'}, 'rust', '/bin/bash -c "rustc {} -o /tmp/a.out;/tmp/a.out"', 'script.rs'),
    DockerExecutor({'sh'}, 'fedora', '/bin/sh {}', 'script.sh'),
    DockerExecutor({'bash'}, 'fedora', '/bin/bash {}', 'script.sh'),
    DockerExecutor({'go'}, 'golang', 'go run {}', 'script.go'),
    DockerExecutor({'lua'}, 'woahbase/alpine-lua', 'lua {}', 'script.lua'),
    DockerExecutor({'ruby'}, 'ruby', 'ruby {}', 'script.rb'),
    DockerExecutor({'haskell'}, 'haskell', 'runghc {}', 'script.hs'),
    DockerExecutor({'lisp'}, 'daewok/lisp-devel', 'sbcl --script  {}', 'script.lisp'),
    DockerExecutor({'perl'}, 'perl', 'perl {}', 'script.pl'),
    DockerExecutor({'r'}, 'r-base', 'Rscript {}', 'script.r'),
    DockerExecutor({'julia'}, 'julia', 'julia {}', 'script.jl'),
    DockerExecutor({'kotlin'}, 'zenika/kotlin', 'kotlinc -script {}', 'script.kts'),
)


language_emojis = {
    'python':':snake:',
    'java':':coffee:',
    'js':':poop:',
    'javascript':':poop:',
    'ts':':sauropod:',
    'typescript':':sauropod:',
    'php':':elephant:',
    'c':':regional_indicator_c:',
    'c++':':rat:',
    'cpp':':rat:',
    'rust':':crab:',
    'sh':':shell:',
    'bash':':computer:',
    'go':':chipmunk:',
    'lua':':new_moon:',
    'ruby':':diamonds:',
    'haskell':':regional_indicator_h:',
    'lisp':':alien:',
    'perl':':onion:',
    'r':':regional_indicator_r:',
    'julia':':regional_indicator_j:',
    'kotlin':':regional_indicator_k:',
}

@dataclass()
class DockerRun:
    language: str
    code: str
    pulling_emoji = emoji.EMOJI_ALIAS_UNICODE[':arrow_down:']
    loading_emoji = emoji.EMOJI_ALIAS_UNICODE[':hourglass:']
    success_emoji = emoji.EMOJI_ALIAS_UNICODE[':white_check_mark:']
    error_emoji = emoji.EMOJI_ALIAS_UNICODE[':x:']
    language_emojis : dict = field(default_factory=lambda: dict(language_emojis))
    executors: Sequence[DockerExecutor] = field(default=executors)
    docker_client: docker.DockerClient = field(default_factory=docker.from_env)
    

    async def __call__(self, client: Client, message: Message):
        this = self
        class Listener(DockerExecutor.Listener):

            async def on_accept(self):
                emoji_code = this.language_emojis.get(this.language, ':gear:')
                lang_emoji = emoji.EMOJI_ALIAS_UNICODE[emoji_code]
                await message.add_reaction(lang_emoji)

            async def pre_pull_image(self):
                await message.add_reaction(this.pulling_emoji)

            async def post_pull_image(self):
                await message.remove_reaction(this.pulling_emoji, client.user)

            async def pre_run(self):
                await message.add_reaction(this.loading_emoji)

            async def post_run(self):
                await message.remove_reaction(this.loading_emoji, client.user)

            async def on_error(self, exception: Exception):
                await message.add_reaction(this.error_emoji)
                await message.reply(f'```{exception.args[0]}```')

            async def on_success(self):
                await message.add_reaction(this.success_emoji)


        for executor in self.executors:
            if self.language not in executor.aliases:
                continue
            executor.listener = Listener()
            output = await executor.exec(self.code)
            await message.reply(output)
            return

class RunCodeInDocker(MessageHandler):
    pattern = re.compile('```(?P<language>[a-zA-Z0-9+#-]+)\\n(?P<code>[^`]*)```')

    def accept(self, message: Message) -> bool:
        match = self.pattern.findall(message.clean_content)
        return bool(match)

    async def handle(self, client: Client, message: Message):
        for match in self.pattern.findall(message.clean_content):
            language, code = match
            run = DockerRun(language=language.lower(), code=code)
            asyncio.ensure_future(run(client, message))
