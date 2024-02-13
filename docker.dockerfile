FROM python:3.11.7
COPY . /
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD ["python", "./invoker.py"]