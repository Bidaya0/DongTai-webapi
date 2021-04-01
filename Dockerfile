FROM python:3.7.7
ARG VERSION
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
ENV TZ=Asia/Shanghai

RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\n\
          deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\n\
          deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\n\
          deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free\n\
          deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free\n\
          deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free\n\
          deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free\n\
          deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security/ buster/updates main contrib non-free" > /etc/apt/sources.list

RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add - \
    && apt-key fingerprint ABF5BD827BD9BF62 \
    && apt-get update -y \
    && apt install -y libc6-dev unzip  vim cron swig

COPY requirements.txt /opt/iast/webapi/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /opt/iast/webapi/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host mirrors.aliyun.com

COPY . /opt/iast/webapi
WORKDIR /opt

CMD ["/usr/local/bin/uwsgi","--ini", "/opt/iast/webapi/conf/fire_uwsgi.ini"]
