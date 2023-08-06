Hermes lib
==========

This lib provides common utilities for the hermes home automation platform

https://framagit.org/hermes-ng

It embeds 3 classes:

* ConfigManager: using a list of variables, loads them from environment. Manages the default values, and the errors

* DbOperations: taking SQL statements, sends them to the Database

* MqttPublisher: sends payloads to standardized mqtt topics
 
