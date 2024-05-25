# ccat_conversation_logger - Cheshire Cat AI Conversation Logger

![Plugin Logo](./logo.jpg)

This Cheshire Cat AI plugin hooks in to the conversation workflow between Cheshire Cat and the User keeping a log of the ongoing conversation.

The log can be analyzed later on to fine tune the Knowledge Base of Cheshire Cat AI.

This plugin is intended as an inspection tool. Please check for any legal compliance in your organization, for any privacy constraint on tracking an user conversation (i.e.: if the  user intentionally or unintentionally shares any sensitive information with the bot it will be feed in the Log for the conversation)

## Usage

1. Install the plugin
2. Configure the connection to the Database - the default settings logs all the conversation in a local database. You may prefer to use an external one.

## Supported Databases

Currently this plugin supports the following databases:

- SQLite
- Oracle MySQL (or MariaDB)
- PostgreSQL

## Configuration

To configure the plugin please use the Plugin Configuration tool within Cheshire Cat AI and specify the DSN to a valid database:

- sqlite:///path/database.sql 
- mysql+pymysql://user:password@host/database
- postgresql://user:password@host/database
