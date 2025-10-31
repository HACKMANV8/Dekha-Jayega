"""
Test script for SagaEngine API Server

This script demonstrates how to use the SagaEngine API for game narrative generation.
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8001"
TEST_TOPIC = "A dark fantasy RPG with Norse mythology themes and souls-like combat"


def print_separator(title: str = ""):
    """Print a visual separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    else:
        print("=" * 70)


def print_stage_data(stage: str, data: Dict[str, Any]):
    """Pretty print stage data"""
    print(f"\n📊 {stage.upper()} DATA:")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")


def test_health_check():
    """Test the health check endpoint"""
    print_separator("HEALTH CHECK")
    
    response = requests.get(f"{API_BASE_URL}/health")
    assert response.status_code == 200
    
    data = response.json()
    print(f"✓ Server is healthy: {data}")
    
    return True


def test_basic_workflow():
    """Test basic workflow without research"""
    print_separator("BASIC WORKFLOW TEST")
    
    # Step 1: Start workflow
    print("\n1️⃣  Starting workflow...")
    start_request = {
        "topic": TEST_TOPIC,
        "research_required": "not_required",
        "model": None,  # Use default
        "parallel_execution": False
    }
    
    response = requests.post(
        f"{API_BASE_URL}/workflow/start",
        json=start_request
    )
    
    assert response.status_code == 200
    data = response.json()
    session_id = data["session_id"]
    
    print(f"✓ Workflow started")
    print(f"   Session ID: {session_id}")
    print(f"   Current Stage: {data['current_stage']}")
    print(f"   Awaiting Feedback: {data['awaiting_feedback']}")
    
    if data.get("data", {}).get("concept"):
        print_stage_data("concept", data["data"]["concept"])
    
    # Step 2: Get current state
    print("\n2️⃣  Getting current state...")
    response = requests.get(f"{API_BASE_URL}/workflow/state/{session_id}")
    assert response.status_code == 200
    print("✓ State retrieved successfully")
    
    # Step 3: Submit feedback (optional)
    print("\n3️⃣  Submitting feedback...")
    feedback_request = {
        "session_id": session_id,
        "feedback": "Make the world setting more dark and gritty. Add more Norse mythology elements."
    }
    
    response = requests.post(
        f"{API_BASE_URL}/workflow/feedback",
        json=feedback_request
    )
    
    if response.status_code == 200:
        print("✓ Feedback submitted and stage regenerated")
        data = response.json()
        if data.get("data", {}).get("concept"):
            print_stage_data("concept (updated)", data["data"]["concept"])
    
    # Step 4: Continue to next stage (World Lore)
    print("\n4️⃣  Continuing to next stage...")
    continue_request = {"session_id": session_id}
    
    response = requests.post(
        f"{API_BASE_URL}/workflow/continue",
        json=continue_request
    )
    
    assert response.status_code == 200
    data = response.json()
    
    print(f"✓ Moved to stage: {data['current_stage']}")
    if data.get("data", {}).get("world_lore"):
        print_stage_data("world_lore", data["data"]["world_lore"])
    
    # Step 5: Continue to Factions
    print("\n5️⃣  Continuing to Factions stage...")
    response = requests.post(
        f"{API_BASE_URL}/workflow/continue",
        json=continue_request
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Moved to stage: {data['current_stage']}")
        if data.get("data", {}).get("factions"):
            print(f"   Generated {len(data['data']['factions'])} factions")
    
    # Step 6: Clean up session
    print("\n6️⃣  Cleaning up session...")
    response = requests.delete(f"{API_BASE_URL}/workflow/{session_id}")
    assert response.status_code == 200
    print("✓ Session deleted")
    
    return session_id


def test_research_workflow():
    """Test workflow with research integration"""
    print_separator("RESEARCH WORKFLOW TEST")
    
    # Step 1: Start workflow with research
    print("\n1️⃣  Starting workflow with research...")
    start_request = {
        "topic": "A cyberpunk RPG set in Neo-Tokyo 2099",
        "research_required": "required",
        "research_question": "Cyberpunk themes, Neo-Tokyo culture, transhumanism, and dystopian futures"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/workflow/start",
        json=start_request
    )
    
    assert response.status_code == 200
    data = response.json()
    session_id = data["session_id"]
    
    print(f"✓ Workflow started with research")
    print(f"   Session ID: {session_id}")
    print(f"   Current Stage: {data['current_stage']}")
    
    # Check if research was integrated
    if data.get("data", {}).get("research"):
        research_data = data["data"]["research"]
        print(f"   Research Notes: {research_data.get('raw_notes_count', 0)} notes")
        print(f"   Research Summary Length: {len(research_data.get('compressed_research', ''))} chars")
    
    if data.get("data", {}).get("concept"):
        print_stage_data("concept (with research)", data["data"]["concept"])
    
    # Clean up
    print("\n2️⃣  Cleaning up session...")
    response = requests.delete(f"{API_BASE_URL}/workflow/{session_id}")
    print("✓ Session deleted")
    
    return session_id


def test_standalone_research():
    """Test standalone research endpoint"""
    print_separator("STANDALONE RESEARCH TEST")
    
    print("\n1️⃣  Executing standalone research...")
    
    response = requests.post(
        f"{API_BASE_URL}/research/execute",
        params={
            "topic": "Viking Age Scandinavia",
            "research_question": "Viking Age Scandinavia: culture, warfare, mythology for game design"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    print(f"✓ Research completed")
    print(f"   Session ID: {data['session_id']}")
    print(f"   Raw Notes: {len(data['raw_notes'])} notes")
    print(f"   Compressed Research: {len(data['compressed_research'])} chars")
    print(f"\n   Preview: {data['compressed_research'][:200]}...")
    
    return True


def test_complete_workflow():
    """Test a complete workflow from start to finish"""
    print_separator("COMPLETE WORKFLOW TEST")
    
    print("\n🚀 Starting complete saga generation workflow...")
    print(f"   Topic: {TEST_TOPIC}")
    
    # Start workflow
    start_request = {
        "topic": TEST_TOPIC,
        "research_required": "not_required",
    }
    
    response = requests.post(
        f"{API_BASE_URL}/workflow/start",
        json=start_request
    )
    
    assert response.status_code == 200
    data = response.json()
    session_id = data["session_id"]
    
    print(f"\n✓ Session created: {session_id}")
    
    # Stages to complete
    stages = ["concept", "world_lore", "factions", "characters", "plot_arcs", "questlines"]
    
    for i, stage in enumerate(stages, 1):
        current_stage = data["current_stage"]
        print(f"\n{i}. Stage: {current_stage}")
        
        # Continue to next stage (except for first one)
        if i > 1:
            response = requests.post(
                f"{API_BASE_URL}/workflow/continue",
                json={"session_id": session_id}
            )
            
            if response.status_code != 200:
                print(f"   ⚠️  Error continuing to next stage: {response.text}")
                break
            
            data = response.json()
            current_stage = data["current_stage"]
        
        # Check if complete
        if current_stage == "complete":
            print(f"   ✓ Workflow complete!")
            break
        
        print(f"   ✓ Generated {current_stage}")
        
        # Show data summary
        stage_data = data.get("data", {}).get(stage)
        if stage_data:
            if isinstance(stage_data, list):
                print(f"      Items: {len(stage_data)}")
            elif isinstance(stage_data, dict):
                print(f"      Keys: {list(stage_data.keys())[:5]}")
    
    # Export results
    print(f"\n7️⃣  Exporting results...")
    
    if data["current_stage"] == "complete":
        # Export as JSON
        response = requests.get(
            f"{API_BASE_URL}/workflow/{session_id}/export",
            params={"format": "json"}
        )
        
        if response.status_code == 200:
            export_data = response.json()
            print(f"   ✓ JSON export: {len(export_data.get('files', []))} files")
            for file in export_data.get('files', [])[:3]:
                print(f"      - {file}")
        
        # Export as Markdown
        response = requests.get(
            f"{API_BASE_URL}/workflow/{session_id}/export",
            params={"format": "markdown"}
        )
        
        if response.status_code == 200:
            export_data = response.json()
            print(f"   ✓ Markdown export: {len(export_data.get('files', []))} files")
            for file in export_data.get('files', [])[:3]:
                print(f"      - {file}")
    else:
        print("   ⚠️  Workflow not complete, skipping export")
    
    # Clean up
    print(f"\n8️⃣  Cleaning up...")
    response = requests.delete(f"{API_BASE_URL}/workflow/{session_id}")
    print("   ✓ Session deleted")
    
    return True


def main():
    """Run all tests"""
    print_separator("SAGAENGINE API TEST SUITE")
    print("Testing SagaEngine API Server")
    print(f"API Base URL: {API_BASE_URL}")
    
    try:
        # Test 1: Health check
        test_health_check()
        time.sleep(1)
        
        # Test 2: Basic workflow
        test_basic_workflow()
        time.sleep(1)
        
        # Test 3: Research workflow (optional - can be slow)
        # Uncomment to test research integration
        # test_research_workflow()
        # time.sleep(1)
        
        # Test 4: Standalone research (optional - can be slow)
        # Uncomment to test standalone research
        # test_standalone_research()
        # time.sleep(1)
        
        # Test 5: Complete workflow (can be very slow)
        # Uncomment to test complete end-to-end workflow
        # test_complete_workflow()
        
        print_separator("ALL TESTS PASSED")
        print("✓ All API tests completed successfully!")
        
    except AssertionError as e:
        print_separator("TEST FAILED")
        print(f"❌ Test assertion failed: {e}")
        return False
        
    except requests.exceptions.ConnectionError:
        print_separator("CONNECTION ERROR")
        print(f"❌ Could not connect to API server at {API_BASE_URL}")
        print("   Make sure the server is running:")
        print("   python saga_api_server.py")
        return False
        
    except Exception as e:
        print_separator("ERROR")
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


