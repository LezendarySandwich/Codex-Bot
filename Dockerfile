FROM python:3.7

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
RUN rm -rf /tmp
