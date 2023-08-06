# LE Logging Library

## Installation:

```
pip install le-logging
```

This library defines a standardized logging pattern for all Python based Projects inside LE Environment.

It's based on Pythons integrated Logging System and makes it easy to use without redefining Layouts and Rotations
manually for every project.

It's mandatory to generalize Logs to simplify debugging and problem solving.

Available Log Levels are defined as ENUM

```python
class Level(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
```

# The usage of the Library is simple:

## Defining a Rotating LogFile based on filesize:

```
attribut is the maximum file size in Megabytes [Default is 32MB]
max_backup attribut defines the maximum stored Files before overwriting existing Files [Default is 14 Files]
```

```python
# Defining loglevel as integer:
from le_logging import RotatingLog

log = RotatingLog(name="Testlog", max_backups=5, max_size=64, level=10)
```

```python
# Defining LogLevel based on Enum
from le_logging import RotatingLog, Level

log = RotatingLog(name="Testlog", max_backups=5, max_size=64, level=Level.DEBUG)
```

```python
# Defining specific Path
from le_logging import RotatingLog, Level

log = RotatingLog(name="Testlog", path="/var/log", max_backups=5, max_size=64, level=Level.DEBUG)
```

## Defining a Timed Rotating LogFile based on filesize:

```python
# Defining loglevel as integer:
from le_logging import TimedRotatingLog

log = TimedRotatingLog(name="Testlog", max_backups=5, max_size=64, level=10)
```

```python
# Defining LogLevel based on Enum
from le_logging import TimedRotatingLog, Level

log = TimedRotatingLog(name="TimedTestlog", max_backups=5, timer=1, level=Level.DEBUG)
```

```python
# Defining specific Path
from le_logging import TimedRotatingLog, Level

log = TimedRotatingLog(name="TimedTestlog", path="/var/log", max_backups=5, timer=1, level=Level.DEBUG)
```

## Using defined LogFiles

```python
log.debug("This is a DEBUG message")
log.info("This is an INFO message")
log.warn("This is a warn message")
log.error("This is an ERROR message")
log.critical("This is a CRITICAL message")
```

