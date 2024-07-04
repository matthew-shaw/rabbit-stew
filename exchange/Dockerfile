FROM rabbitmq:3.13-management-alpine

COPY rabbitmq.conf /etc/rabbitmq/
COPY ssl/ca_certificate.pem ssl/server_exchange_certificate.pem ssl/server_exchange_key.pem /etc/rabbitmq/ssl/

RUN chown -R rabbitmq:rabbitmq /etc/rabbitmq/ssl/

HEALTHCHECK --interval=10s CMD rabbitmq-diagnostics -t 30 check_running