# Use newer base image with better security
FROM python:3.11-slim-bookworm

# Update packages and install dependencies in single stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libssl-dev libffi-dev python3-dev \
    nginx uwsgi uwsgi-plugin-python3 ca-certificates curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd --gid 1001 uwsgi && \
    useradd --uid 1001 --gid uwsgi --create-home --shell /bin/bash uwsgi

# CRITICAL: Upgrade setuptools in SYSTEM Python (not venv) - this is what Trivy scans
RUN pip install --upgrade pip==24.3.1 setuptools==78.1.1 wheel==0.45.1

WORKDIR /srv/flask_app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=uwsgi:uwsgi . /srv/flask_app

# Create necessary directories and set permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/run /tmp /var/lib/nginx/tmp /tmp/client_body_temp /srv/flask_app/database \
    && chown -R www-data:www-data /var/log/nginx /var/cache/nginx /var/lib/nginx \
    && chown -R uwsgi:uwsgi /srv/flask_app /srv/flask_app/database \
    && chmod -R 755 /var/lib/nginx /tmp \
    && chmod 664 /tmp/uwsgi.socket 2>/dev/null || true \
    && touch /tmp/uwsgi.log && chown uwsgi:uwsgi /tmp/uwsgi.log && chmod 664 /tmp/uwsgi.log

# Copy nginx configuration
COPY conf/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx as root and uwsgi as uwsgi user
CMD ["sh", "-c", "nginx -g 'daemon off;' & su -s /bin/bash uwsgi -c 'cd /srv/flask_app && uwsgi --ini uwsgi.ini' && wait"]
