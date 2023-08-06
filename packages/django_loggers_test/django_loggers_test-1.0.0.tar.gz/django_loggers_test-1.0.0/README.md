# Django Loggers Test

A simple tester of Django's loggers' configuration.

## Content

1. [Installation](#installation)
2. [Usage](#usage)

## Installation

The easiest way to get this is from PyPI:

```bash
pip install django_loggers_test
```

## Usage

Run your project's shell (`python manage.py shell`), and then

```pycon
>>> from django_loggers_test import loggers_test
>>> loggers_test()
```

This will log messages to the console, using all available formatters and
levels. There isn't really much more to it, apart from minor configurability.
For details, run

```pycon
>>> help(loggers_test)
```
