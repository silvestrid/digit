FROM ubuntu:impish

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt install -y \
    curl sudo gnupg2 nano

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - \
    && curl -sL https://deb.nodesource.com/setup_16.x  | bash -

RUN apt-get update && \
    apt install -y \
    make git nginx supervisor \
    libpq-dev \
    python3 build-essential libxslt-dev python3-dev python3-virtualenv \
    python3-setuptools zlib1g-dev libffi-dev libssl-dev python3-pip \
    && rm -rf /var/cache/apt /var/lib/apt/lists

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt install -y nodejs
RUN npm install --global yarn

RUN mkdir -p /digit /run/temp/update-check
WORKDIR /digit

RUN service supervisor stop && service nginx stop
RUN rm -f /etc/nginx/sites-enabled/*

ADD . /digit/digit
ADD backend/poetry.lock backend/pyproject.toml /digit/
RUN virtualenv -p python3 env
RUN env/bin/pip install poetry && env/bin/poetry install --no-dev && env/bin/poetry add dj-database-url boto3==1.16.25 django-storages==1.10.1
RUN (cd digit/web-frontend && yarn install && npm run build)

RUN (mkdir -p /digit/heroku/heroku && \
    mkdir /digit/media && \
    touch /digit/heroku/heroku/__init__.py)
ADD deploy/heroku/settings.py /digit/heroku/heroku

ENV PYTHONPATH $PYTHONPATH:/digit/digit/backend/src:/digit/digit/premium/backend/src:/digit/heroku
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TMPDIR=/run/temp

ADD deploy/heroku/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
RUN ln -sf /dev/stdout /var/log/supervisor/supervisord.log

ADD deploy/heroku/nginx.conf /digit/nginx.conf
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

ADD deploy/heroku/entry.sh /digit/entry.sh
RUN ["chmod", "+x", "/digit/entry.sh"]
