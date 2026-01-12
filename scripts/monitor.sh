#!/bin/bash

echo "📊 safeshare Monitoring Dashboard"
echo "================================="
echo ""

# Container status
echo "🐳 Container Status:"
docker ps --filter "name=safeshare-bot" --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"
echo ""

# Resource usage
echo "💻 Resource Usage:"
docker stats --no-stream safeshare-bot --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
echo ""

# Recent logs
echo "📝 Recent Logs (last 20 lines):"
docker logs --tail 20 safeshare-bot
echo ""

# Health check
echo "🏥 Health Status:"
docker inspect safeshare-bot --format='{{.State.Health.Status}}' 2>/dev/null || echo "No health check configured"
echo ""

echo "💡 Commands:"
echo "  View live logs: docker logs -f safeshare-bot"
echo "  Restart:        docker-compose restart"
echo "  Stop:           docker-compose down"