FROM python:3
LABEL Maintainer="Pat Heaney <s3cpat@psu.edu>" Description="Automated Analysis of a Phishing Email" Version="1.0"
WORKDIR /usr/src/app

RUN mkdir uploads

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./your-daemon-or-script.py" ]
CMD ["gunicorn", "--bind=0.0.0.0:80", "-w 1", "app:app"]
EXPOSE 80