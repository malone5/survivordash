FROM python:3.9.5

# location of our sourcecode
WORKDIR /code
# Where puyhon will look for additional modules/packages
ENV PYTHONPATH=/code/src


# Place requirements file in our container
COPY ./containers/pipeline/requirements.txt requirements.txt
# install python requirements
RUN pip install -r requirements.txt

# COPY our whole repository into code dir
COPY ./ /code/

# keep continer from stopping
ENTRYPOINT ["tail", "-f", "/dev/null"]

