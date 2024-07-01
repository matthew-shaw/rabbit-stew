FROM rabbitmq:3.13-management-alpine

# COPY rabbitmq.conf /etc/rabbitmq/

HEALTHCHECK --interval=10s CMD rabbitmq-diagnostics -t 30 check_running