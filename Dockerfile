FROM python:3.9-alpine

# Create non-root user
RUN addgroup -g 1001 -S uwsgi && \
    adduser -u 1001 -S uwsgi -G uwsgi

# Install system dependencies including build tools for uWSGI
RUN apk add --no-cache \
    nginx \
    uwsgi \
    uwsgi-python3 \
    build-base \
    python3-dev \
    linux-headers

# Copy nginx configuration
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Copy application code
COPY --chown=uwsgi:uwsgi . /srv/flask_app

# Set working directory
WORKDIR /srv/flask_app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories and set permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/run /tmp /var/lib/nginx/tmp /tmp/client_body_temp /srv/flask_app/database \
    && chown -R uwsgi:uwsgi /var/log/nginx /var/cache/nginx /var/run /tmp /var/lib/nginx /tmp/client_body_temp /srv/flask_app/database \
    && chown -R uwsgi:uwsgi /srv/flask_app \
    && chmod -R 755 /var/lib/nginx

# Switch to non-root user
USER uwsgi

# Expose port
EXPOSE 80

# Start services
CMD ["sh", "-c", "nginx && uwsgi --ini uwsgi.ini"]
