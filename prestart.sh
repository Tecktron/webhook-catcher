#!/bin/sh
# Borrowed from https://docs.docker.com/compose/startup-order/
# wait-for-postgres.sh

SKIP_CREATE_DB=${SKIP_CREATE_DB:-"false"}

if [ "${SKIP_CREATE_DB}" = "true" ]; then
  SKIP_CREATE_DB="true"
fi

x=0
if [ "${SKIP_CREATE_DB}" = "true" ]; then
  PGCONNECT=postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}
else
  PGCONNECT=postgresql://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/postgres
fi

until psql $PGCONNECT -c '\q'; do
  if [ $x -gt 10 ]; then
    echo "Cannot find postgres, aborting"
    exit 8
  fi
  echo "Postgres is unavailable - sleeping..."
  sleep 3
  x=$(($x+1))
done

echo "Postgres is up!"
cd /app || exit 1

if [ "${SKIP_CREATE_DB}" != "true" ]; then
  psql ${PGCONNECT} -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1 || psql ${PGCONNECT} -c "CREATE DATABASE \"${DB_NAME}\" WITH OWNER '${DB_USER}'"
fi

ADMIN_USER=${ADMIN_USER:-"admin"}
ADMIN_PASS=${ADMIN_PASS:-"admin"}

python manage.py migrate
python manage.py create_default_superuser --username="${ADMIN_USER}" --password="${ADMIN_PASS}"
mkdir -p /app/static
python manage.py collectstatic --no-input
