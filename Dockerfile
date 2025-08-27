# Build Caddy with the Layer-4 plugin
FROM caddy:builder AS builder
RUN xcaddy build --with github.com/mholt/caddy-l4

FROM caddy:latest
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY Caddyfile /etc/caddy/Caddyfile
