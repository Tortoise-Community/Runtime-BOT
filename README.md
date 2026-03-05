# Runtime Bot

A Discord bot that allows users to execute code directly inside Discord channels using the **Hermes Engine**.
The bot parses `/run` code blocks, sends the code to the Hermes API, and returns the execution result in an embedded response.

Developed by **Tortoise Community**.

---

# Features

* Execute **Python**, **JavaScript**, and **Java** code directly in Discord.
* Secure execution through the **Hermes sandbox engine**.
* Automatic re-execution when a message is edited (within 2 minutes).
* Per-guild runtime enable/disable control.
* Engine error and maintenance handling.
* Built-in health monitoring endpoints and command for observing bot status and system metrics.

---

# Supported Languages

| Language   | Aliases            |
| ---------- | ------------------ |
| Python     | `python`, `py`     |
| JavaScript | `javascript`, `js` |
| Java       | `java`             |


---

# Usage

Send a message beginning with `/run` followed by a fenced code block.

Example:

````
/run 
```python
print(1 + 1)
```
````


Bot response:
```ex
2
```

### JavaScript Example

````

/run 
```javascript
console.log(1 + 1)
```
````

### Java Example

````
/run 
```java
public class Main {
    public static void main(String[] args) {
        System.out.println(1 + 1);
    }
}
```
````

## Message Editing

If a user edits their message within **2 minutes**, the bot will automatically re-execute the updated code and update the previous output message.


## Runtime Controls

Administrators can enable or disable execution per server.

### Enable runtime

```

/enable_runtime

```

### Disable runtime

```

/disable_runtime

```

---

# Requirements

- Python 3.10+
- PostgreSQL
- Hermes Code Execution Engine

# Environment Variables

Create a `.env` file.

```

DISCORD_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:password@localhost/dbname
EXECUTION_API_URL=https://your-hermes-api/execute
BOT_BUILD_VERSION=optional_build_identifier
HOST=your_health_monitor_host
PORT=your_health_monitor_port
```


# Installation

Clone the repository:

```

git clone https://github.com/Tortoise-Community/Runtime-BOT.git
cd Runtime-BOT

```

Install dependencies:

```

pip install -r requirements.txt

```

Run the bot:

```

python bot.py

```

---

# Database

The bot requires PostgreSQL.  
Tables are created automatically on startup.

Example table used for runtime control:

```

runtime_config

```

| Column | Type |
|------|------|
| guild_id | BIGINT |
| enabled | BOOLEAN |

---


## Hermes Engine

This bot requires the **Hermes Code Execution Engine**.

Repository:

```
https://github.com/Ryuga/Hermes
```
