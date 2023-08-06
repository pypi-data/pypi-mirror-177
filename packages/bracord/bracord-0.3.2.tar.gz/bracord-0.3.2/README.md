# Bracord
A [Disnake](https://github.com/DisnakeDev/Disnake) framework written in Python that speeds the development of Discord bots.

Bracord is a combination of a command line tool and ready-to-go cogs that might come useful when developing quick Discord bots.

**Table of Contents**
- [Installation](#installation)
- [Usage](#usage)

## Installation

You can install Bracord using `pip`.

```bash
$ pip3 install bracord
```

## Usage

### Project Initialization
First, you will need to initialize a Bracord project. You can do so with the following command:

```bash
$ bracord init
```

This will start asking for information related to your bot and then create all necessary files in the current directory.

### Cog Creation
To create and register a cog, you can use the `cog` command:

```bash
$ bracord cog
```

This will ask you for the cog's name and will create it and load it whenever when the bot is started.
