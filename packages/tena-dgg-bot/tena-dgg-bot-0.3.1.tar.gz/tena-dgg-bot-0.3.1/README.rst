DGG-bot
======

.. image:: https://img.shields.io/pypi/v/dgg-bot.svg
   :target: https://pypi.python.org/pypi/tena-dgg-bot
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/dgg-bot.svg
   :target: https://pypi.python.org/pypi/tena-dgg-bot
   :alt: PyPI supported Python versions
A library for making a bot in Destiny.gg chat.

Installing
----------

**Python 3.8 or higher is required**

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U dgg-bot

    # Windows
    py -3 -m pip install -U dgg-bot


Usage
-----

Not sure what to put here at this point in time. Unauthorized chat bots are subject to being **banned**, ask Cake in DGG for permission and guidelines for chat bots before running one.


Examples
--------

A simple bot that says obamna.

.. code-block:: python

    from tenadggbot import DGGBot, Message
    import asyncio


    auth = "obamna"
    obamnabot = DGGBot(auth_token=auth)

    @obamnabot.command(["obamna"])
    async def obamna_command(msg: Message):
        await msg.reply("OBAMNA LULW")

    
    if __name__ == "__main__":
        asyncio.run(obamnabot.run())