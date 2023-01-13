#!/usr/bin/env sh

export D='$'

/bin/sh -c envsubst \
'$${NGINX_UPSTREAM} $${NGINX_SERVER_PORT} $${NGINX_API_PREFIX}' \
< /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
