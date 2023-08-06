[![Upload Python Package](https://github.com/jacobtruman/TruLogger/actions/workflows/python-publish.yml/badge.svg)](https://github.com/jacobtruman/TruLogger/actions/workflows/python-publish.yml)

# TruLogger

A simple python log library

## Installation

Install via pip

```bash
pip install TruLogger
```

## Usage

Here are some simple examples of usage:

```python
import trulogger


logger = trulogger.TruLogger({'verbose': True})

# define a custom prefix
logger.set_prefix("custom prefix")

logger.info("This is info")
# [ 2022-10-22 16:37:02 ]	[ INFO ] custom prefix	This is info
logger.error("This is error")
# [ 2022-10-22 16:37:02 ]	[ ERROR ] custom prefix	This is error
logger.warning("This is warning")
# [ 2022-10-22 16:37:02 ]	[ WARNING ] custom prefix	This is warning
logger.debug("This is debug")
# [ 2022-10-22 16:37:02 ]	[ DEBUG ] custom prefix	This is debug
logger.success("This is success")
# [ 2022-10-22 16:37:02 ]	[ SUCCESS ] custom prefix	This is success

logger.add_to_log("This is a simple add")
# This is a simple add

# Create a new logger with traceback included
logger2 = trulogger.TruLogger({'verbose': True, 'traceback': True})

logger2.set_prefix("custom prefix")

logger2.info("This is info")
# [ 2022-10-22 16:37:02 ]	[ INFO ] custom prefix	This is info

# clear the custom prefix
logger2.reset_prefix()
logger2.error("This is error")
# [ 2022-10-22 16:37:02 ]	[ ERROR ]	This is error
# [<FrameSummary file /Users/jacobtruman/workspace/personal/TruLogger/tests.py, line 22 in <module>>, <FrameSummary file /Users/jacobtruman/workspace/personal/TruLogger/trulogger/__init__.py, line 93 in error>]
logger2.warning("This is warning")
# [ 2022-10-22 16:37:02 ]	[ WARNING ]	This is warning
logger2.debug("This is debug")
# [ 2022-10-22 16:37:02 ]	[ DEBUG ]	This is debug
logger2.success("This is success")
# [ 2022-10-22 16:37:02 ]	[ SUCCESS ]	This is success

logger2.add_to_log("This is a simple add")
# This is a simple add
```
