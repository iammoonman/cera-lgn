FROM python:3.11.7
ENV PYTHONUNBUFFERED=1
COPY . /
RUN pip install -r requirements.txt
CMD ["python", "-u", "./invoker.py"]