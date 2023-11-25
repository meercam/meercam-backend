FROM python:3.11-bookworm

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

COPY . .

# Install Dependencies of Miniconda
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD [ "/bin/bash" ]
# run flask immediately 
# CMD ["flask", "--app",  "main" , "run" ,"--host=0.0.0.0"]