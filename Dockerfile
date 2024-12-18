FROM python:3.10-slim

COPY / .


CMD [ "py", "bot_start.py" ]