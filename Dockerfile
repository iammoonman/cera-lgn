FROM python:3.11.7
COPY . /
RUN pip install -r requirements.txt
CMD ["python", "./invoker.py"]