FROM ghcr.io/seraftech/python-311-opensuse:v0.0.1

RUN zypper --non-interactive si -d python311 python311-pip \
    && zypper --non-interactive in python311 \
    && python3.11 -m ensurepip

COPY requirements.txt /requirements.txt

RUN python3.11 -m pip install -r /requirements.txt

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "300", "mdroid_.wsgi"]