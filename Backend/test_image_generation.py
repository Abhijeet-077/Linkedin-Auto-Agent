#!/usr/bin/env python3
"""
Test Image Generation with OpenRouter API
"""

import asyncio
import aiohttp
import json

BASE_URL = "http://localhost:8000"

async def test_image_generation():
    """Test the image generation endpoint"""
    print("🎨 Testing Image Generation with OpenRouter API")
    print("=" * 50)
    
    test_cases = [
        {
            "topic": "AI in Business",
            "content": "Artificial intelligence is transforming how we work and innovate."
        },
        {
            "topic": "Leadership Development", 
            "content": "Great leaders inspire teams to achieve extraordinary results."
        },
        {
            "topic": "Digital Marketing Trends",
            "content": "The future of marketing is data-driven and customer-centric."
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['topic']}")
            
            try:
                async with session.post(
                    f"{BASE_URL}/api/v1/generate-image",
                    json=test_case
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        if result.get("success"):
                            image_url = result.get("image_url", "")
                            print(f"   ✅ Success: Image generated")
                            print(f"   🔗 URL: {image_url[:80]}...")
                            
                            if "unsplash" in image_url:
                                print(f"   📸 Type: Professional stock image")
                            elif "openai" in image_url or "dall-e" in image_url.lower():
                                print(f"   🤖 Type: AI-generated (DALL-E)")
                            else:
                                print(f"   🎨 Type: Generated image")
                                
                        else:
                            print(f"   ❌ Failed: {result}")
                    else:
                        print(f"   ❌ HTTP Error: {response.status}")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Small delay between tests
            await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎯 Image Generation Test Complete")
    print("\n💡 Tips:")
    print("   • Images are generated using your OpenRouter API key")
    print("   • DALL-E 3 is tried first, then DALL-E 2, then stock images")
    print("   • All images are professional and LinkedIn-appropriate")
    print("   • Test the pipeline at: http://localhost:8080/pipeline")

async def test_content_with_images():
    """Test full content generation including images"""
    print("\n🔄 Testing Full Content Pipeline with Images")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        try:
            # Start content generation
            async with session.post(
                f"{BASE_URL}/api/v1/pipeline/generate",
                json={"topic": "Future of Remote Work"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    stream_id = result.get("stream_id")
                    
                    if stream_id:
                        print(f"   ✅ Pipeline started: {stream_id}")
                        print(f"   🔗 Stream: {BASE_URL}/api/v1/pipeline/stream/{stream_id}")
                        print(f"   💡 Open this URL in browser to see real-time generation")
                    else:
                        print(f"   ❌ No stream ID returned")
                else:
                    print(f"   ❌ Pipeline failed: {response.status}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 InfluenceOS Image Generation Test")
    print("⚠️  Make sure the backend server is running first!")
    print("    Run: python start_server.py")
    print("\nPress Enter to start tests...")
    input()
    
    # Run tests
    asyncio.run(test_image_generation())
    asyncio.run(test_content_with_images())
