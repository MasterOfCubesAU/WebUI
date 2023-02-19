FROM python:3.8

RUN mkdir /app
WORKDIR /app

# Copy setup dir first. That way, if requirements are unchanged,
# the cache can be used to save rebuild time.
RUN mkdir setup
COPY setup/ ./setup/
RUN pip install -r ./setup/requirements.txt

# Copy everything else
COPY . ./

EXPOSE 8000

CMD python src/server.py
