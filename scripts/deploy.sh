set -e

echo "🚀 Deploying SafeShare..."

# Check if .env exists
if [ ! -f ../.env ]; then
    echo "❌ Error: .env file not found"
    echo "Please create .env from .env.example and add your TELEGRAM_BOT_TOKEN"
    exit 1
fi

source ../.env

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" == "your_bot_token_here" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not set in .env"
    exit 1
fi

echo "🛑 Stopping existing container..."
docker-compose down || true

echo "🔨 Building Docker image..."
docker-compose build --no-cache

echo "▶️  Starting container..."
docker-compose up -d

echo "⏳ Waiting for container to be ready..."
sleep 5


if docker ps | grep -q safesend-bot; then
    echo "✅ SafeSend deployed successfully!"
    echo ""
    echo "📊 Container status:"
    docker ps | grep safesend-bot
    echo ""
    echo "📝 View logs with: docker-compose logs -f"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi