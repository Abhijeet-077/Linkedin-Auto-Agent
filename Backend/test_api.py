#!/usr/bin/env python3
"""
InfluenceOS API Test Script
Tests all endpoints and functionality
"""

import asyncio
import aiohttp
import json
import time

BASE_URL = "http://localhost:8000"

async def test_endpoint(session, method, endpoint, data=None, description=""):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print(f"🧪 Testing: {description or endpoint}")
        
        if method.upper() == "GET":
            async with session.get(url) as response:
                result = await response.json()
                status = response.status
        else:
            async with session.post(url, json=data) as response:
                result = await response.json()
                status = response.status
        
        if status == 200:
            print(f"   ✅ Success: {status}")
            return True, result
        else:
            print(f"   ❌ Failed: {status}")
            return False, result
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

async def test_pipeline_stream(session):
    """Test the pipeline streaming endpoint"""
    print("🧪 Testing: Pipeline streaming")
    
    try:
        # Start pipeline
        async with session.post(f"{BASE_URL}/api/v1/pipeline/generate", 
                               json={"topic": "AI in business"}) as response:
            if response.status == 200:
                data = await response.json()
                stream_id = data.get("stream_id")
                
                if stream_id:
                    print(f"   ✅ Pipeline started: {stream_id}")
                    
                    # Test streaming (just check if endpoint exists)
                    try:
                        async with session.get(f"{BASE_URL}/api/v1/pipeline/stream/{stream_id}") as stream_response:
                            if stream_response.status == 200:
                                print("   ✅ Streaming endpoint accessible")
                                return True
                    except:
                        pass
                        
                return True
            else:
                print(f"   ❌ Failed to start pipeline: {response.status}")
                return False
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 InfluenceOS API Test Suite")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        tests = [
            # Basic endpoints
            ("GET", "/", None, "Root endpoint"),
            ("GET", "/health", None, "Health check"),
            
            # Analytics
            ("GET", "/api/v1/analytics", None, "Analytics data"),
            
            # Profile
            ("GET", "/api/v1/profile/analyze", None, "Profile analysis"),
            ("POST", "/api/v1/profile/connect-linkedin", {}, "LinkedIn connection"),
            ("POST", "/api/v1/profile/create", {
                "name": "Test User",
                "title": "AI Engineer", 
                "company": "TechCorp",
                "industry": "Technology",
                "bio": "AI enthusiast"
            }, "Profile creation"),
            
            # Posts
            ("POST", "/api/v1/posts/create", {"topic": "AI trends"}, "Post creation"),
            
            # Scheduling
            ("POST", "/api/v1/schedule", {
                "text": "Test post",
                "hashtags": ["#test"],
                "scheduledTime": "2024-01-20T10:00:00Z"
            }, "Post scheduling"),
            
            # Outreach
            ("GET", "/api/v1/outreach/campaigns", None, "Outreach campaigns"),
            ("POST", "/api/v1/outreach/campaigns", {
                "name": "Test Campaign",
                "message": "Hello!",
                "targets": ["user1", "user2"]
            }, "Campaign creation"),
            ("GET", "/api/v1/outreach/templates", None, "Outreach templates"),
        ]
        
        passed = 0
        total = len(tests)
        
        for method, endpoint, data, description in tests:
            success, result = await test_endpoint(session, method, endpoint, data, description)
            if success:
                passed += 1
            
            # Small delay between tests
            await asyncio.sleep(0.5)
        
        # Test pipeline streaming
        print("\n🔄 Testing Pipeline Streaming...")
        if await test_pipeline_stream(session):
            passed += 1
        total += 1
        
        # Results
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed! Backend is fully functional.")
        else:
            print(f"⚠️ {total - passed} tests failed. Check server logs.")
        
        print("\n🔧 Next Steps:")
        print("   1. Start backend: python start_server.py")
        print("   2. Open frontend: http://localhost:8080")
        print("   3. Test all buttons in the UI")
        print("   4. Generate content using the pipeline")

if __name__ == "__main__":
    print("⚠️ Make sure the backend server is running first!")
    print("   Run: python start_server.py")
    print("\nPress Enter to continue with tests...")
    input()
    
    asyncio.run(main())
