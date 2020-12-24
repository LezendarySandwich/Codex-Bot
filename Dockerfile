FROM python:3.7

# During Development
# COPY requirements.txt /tmp/
# RUN pip install --requirement /tmp/requirements.txt
# RUN rm -rf /tmp

# During deployment
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["bash", "run.sh"]