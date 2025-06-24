#!/bin/sh
# wait-for-it.sh


until nc -z "db" "5432"; do
  >&2 echo "Waiting for db:5432 to be available..."
  sleep 1
done

exec "$@"