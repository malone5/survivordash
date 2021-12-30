FROM python:3.9.5

# location of our sourcecode
WORKDIR /code
# Where puyhon will look for additional modules/packages
ENV PYTHONPATH=/code/src

# Place requirements file in our container
COPY ./containers/pipeline/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY our whole repository into code dir
COPY ./ /code/

# We omit this because the script finishes before metabase API is installed
#CMD ["python", "-u", "/code/src/survivordash/run.py"]

# keep continer alive
CMD ["tail", "-f", "/dev/null"]

