FROM python:3.11-alpine AS builder


RUN apk add --no-cache \
    gcc musl-dev linux-headers libffi-dev openssl-dev python3-dev

WORKDIR /install
COPY requirements.txt .


RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-alpine


RUN apk add --no-cache \
    nginx uwsgi uwsgi-python3 ca-certificates curl


RUN addgroup -g 1001 uwsgi 2>/dev/null || true && \
    adduser -u 1001 -G uwsgi -h /home/uwsgi -D uwsgi 2>/dev/null || true


COPY --from=builder /install /usr/local

WORKDIR /srv/flask_app
COPY --chown=uwsgi:uwsgi . /srv/flask_app


RUN mkdir -p /var/log/nginx /var/cache/nginx /var/run /tmp /var/lib/nginx/tmp /srv/flask_app/database \
    && chown -R nginx:nginx /var/log/nginx /var/cache/nginx /var/lib/nginx \
    && chown -R uwsgi:uwsgi /srv/flask_app


COPY conf/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

CMD ["sh", "-c", "nginx && uwsgi --ini /srv/flask_app/uwsgi.ini"]
