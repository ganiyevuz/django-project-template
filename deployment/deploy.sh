#!/bin/bash

# === Project Deployment Script ===
set -e

# Trap errors
trap 'fail_deployment' ERR

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Set defaults
BACKEND_VERSION=${BACKEND_VERSION:-1.0.0}
LOG_FILE="deployment.log"

# Helper to log output
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Helper on deployment failure
fail_deployment() {
  log "Deployment failed!"
  DEPLOYMENT_STATUS="❌ *Deployment Failed!*"
  DEPLOYMENT_DETAILS="📝 *Error Logs:* \`docker compose logs backend\`"

  send_telegram_notification
  exit 1
}

# Telegram notify
send_telegram_notification() {
  if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_IDS" ]; then
    MESSAGE="${DEPLOYMENT_STATUS}\n\n${DEPLOYMENT_DETAILS}\n\n---\n${SUPERUSER_STATUS:-}"

    # Check if the deployment status is failure and append last logs
    if [[ "$DEPLOYMENT_STATUS" == "❌ Deployment Failed!"* ]]; then
      MESSAGE="${MESSAGE}\n\n*Last 30 logs:*\n\`\`\`$(docker compose logs backend | tail -n 30)}\`\`\`"
          # Read chat IDs and send the message to each
      IFS=',' read -r -a CHAT_IDS_ARRAY <<< "$TELEGRAM_CHAT_IDS"
      for CHAT_ID in "${CHAT_IDS_ARRAY[@]}"; do
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
          -d "chat_id=${CHAT_ID}" \
          -d "parse_mode=Markdown" \
          -d "text=${MESSAGE}" > /dev/null
      done
    fi
  fi
}

# Start deployment
log "=== Deploying site to $BACKEND_DOMAIN ==="
log "Backend Version: $BACKEND_VERSION"


# Update docker-compose.yml
log "Updating docker-compose.yml with backend image version..."
sed -i "s|backed_image_name:.*|${BACKEND_IMAGE}|g" docker-compose.yml
sed -i "s|userbot_image_name:.*|${USERBOT_IMAGE}|g" docker-compose.yml
sed -i "s|bot_image_name:.*|${BOT_IMAGE}|g" docker-compose.yml

# Pull, stop old, start new
log "Pulling Docker images..."
docker compose pull --ignore-pull-failures | tee -a "$LOG_FILE"

log "Stopping old containers..."
docker compose down | tee -a "$LOG_FILE"

log "Starting services..."
docker compose up -d | tee -a "$LOG_FILE"


## Wait for services to be ready
#echo "Waiting for services to be ready..."
#for i in {1..30}; do
#  # Check web service health endpoint
#  if curl -s -f http://localhost:8000/api/v1/health > /dev/null; then
#    echo "Web service is healthy"
#
#    # Check API, database, and Redis connectivity through health endpoints
#    if curl -s -f http://localhost:8000/api/v1/health/db > /dev/null; then
#      echo "Database connectivity is working"
#
#      if curl -s -f http://localhost:8000/api/v1/health/cache > /dev/null; then
#        echo "Redis connectivity is working"
#        break  # All services are ready, break out of the loop
#      else
#        echo "Redis connectivity failed, retrying..."
#      fi
#    else
#      echo "Database connectivity failed, retrying..."
#    fi
#  else
#    echo "Web service is not healthy, retrying..."
#  fi
#
#  # Wait 5 seconds before retrying
#  sleep 5
#done
#
## If we reach here, we either have a timeout or the services are ready
#if [ $i -eq 30 ]; then
#  echo "Timeout reached, services are not ready."
#else
#  echo "All services are up and running."
#fi

sleep 10  # Wait for services to stabilize
# Superuser
log "Checking/creating superuser..."
SUPERUSER_RESULT=$(docker compose exec backend python3 manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_EMAIL:-admin@example.com}', '${DJANGO_SUPERUSER_PASSWORD:-admin_password}')
    print('created')
else:
    print('exists')
")

if [[ "$SUPERUSER_RESULT" == *"created"* ]]; then
  SUPERUSER_STATUS="👤 *Superuser created*\n*Email:* \`${DJANGO_SUPERUSER_EMAIL:-admin}\`\n*Password:* \`${DJANGO_SUPERUSER_PASSWORD:-admin_password}\`"
else
  SUPERUSER_STATUS="👤 *Superuser exists*"
fi

# Success Telegram
DEPLOYMENT_STATUS="✅ *Deployment Successful!*"
DEPLOYMENT_DETAILS=""
send_telegram_notification

# Done
log "$DEPLOYMENT_STATUS"
log "$DEPLOYMENT_DETAILS"
log "Deployed backend version: $BACKEND_VERSION"
