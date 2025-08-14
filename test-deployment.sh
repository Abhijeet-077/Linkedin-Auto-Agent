#!/bin/bash

echo "🧪 LinkedIn Auto Agent - Deployment Test"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test Backend API
echo "🔧 Testing Local Backend API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend API is running${NC}"
else
    echo -e "${RED}❌ Backend API is not responding${NC}"
    exit 1
fi

echo ""

# Test Frontend
echo "🎨 Testing Local Frontend..."
if curl -s http://localhost:8080 > /dev/null; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
    exit 1
fi

echo ""
echo "🧪 Testing API Endpoints..."

# Test Content Generation
echo "📝 Testing content generation..."
if curl -s -X POST http://localhost:8000/api/v1/pipeline/generate \
   -H "Content-Type: application/json" \
   -d '{"topic": "Test"}' > /dev/null; then
    echo -e "${GREEN}✅ Content generation API working${NC}"
else
    echo -e "${YELLOW}⚠️ Content generation API failed${NC}"
fi

# Test Profile Analysis
echo "👤 Testing profile analysis..."
if curl -s http://localhost:8000/api/v1/profile/analysis > /dev/null; then
    echo -e "${GREEN}✅ Profile analysis API working${NC}"
else
    echo -e "${YELLOW}⚠️ Profile analysis API failed${NC}"
fi

# Test Outreach Campaigns
echo "🎯 Testing outreach campaigns..."
if curl -s http://localhost:8000/api/v1/outreach/campaigns > /dev/null; then
    echo -e "${GREEN}✅ Outreach campaigns API working${NC}"
else
    echo -e "${YELLOW}⚠️ Outreach campaigns API failed${NC}"
fi

echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"
echo ""
echo "🔗 Local URLs:"
echo "   Frontend: http://localhost:8080"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
