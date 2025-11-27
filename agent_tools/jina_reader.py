"""
Jina Reader integration module.

This module provides functions to interact with Jina Reader API,
supporting both hosted r.jina.ai (no API key required) and custom
Jina instances with API key authentication.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Default hosted Jina Reader URL (no API key required)
JINA_READER_HOSTED_URL = "https://r.jina.ai"


def jina_use_reader() -> bool:
    """
    Check if hosted Jina Reader (r.jina.ai) should be used.
    
    Returns True if:
    - JINA_USE_READER env var is set to 'true' (default behavior), OR
    - No JINA_API_KEY and JINA_API_BASE are set (fallback to hosted reader)
    
    Returns:
        bool: True if hosted Jina Reader should be used
    """
    use_reader_env = os.environ.get("JINA_USE_READER", "true").lower()
    
    # If explicitly set to 'true', use hosted reader
    if use_reader_env == "true":
        return True
    
    # If no API key and no API base are set, default to hosted reader
    jina_api_key = os.environ.get("JINA_API_KEY", "").strip()
    jina_api_base = os.environ.get("JINA_API_BASE", "").strip()
    
    if not jina_api_key and not jina_api_base:
        return True
    
    return False


def jina_enabled() -> bool:
    """
    Check if any Jina backend is available.
    
    Returns True if:
    - Hosted Jina Reader is enabled (jina_use_reader() is True), OR
    - Custom Jina instance is configured (JINA_API_KEY/JINA_API_BASE set)
    
    Returns:
        bool: True if Jina is enabled
    """
    # Check if hosted reader is enabled
    if jina_use_reader():
        return True
    
    # Check if custom Jina instance is configured
    jina_api_key = os.environ.get("JINA_API_KEY", "").strip()
    jina_api_base = os.environ.get("JINA_API_BASE", "").strip()
    
    return bool(jina_api_key) or bool(jina_api_base)


def reader_qa(
    query: str,
    contexts: Optional[List[str]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Query Jina Reader for Q&A-style responses.
    
    If jina_use_reader() is True, uses hosted r.jina.ai without authentication.
    If JINA_API_KEY and JINA_API_BASE are set, uses custom endpoint with Bearer auth.
    
    Args:
        query: The query/prompt to send to the Reader
        contexts: Optional list of context strings for the query
        params: Optional additional parameters for the request
    
    Returns:
        dict: {"ok": True, "answer": "..."} on success,
              {"ok": False, "error": "..."} on failure
    """
    contexts = contexts or []
    params = params or {}
    
    try:
        if jina_use_reader():
            # Use hosted Jina Reader (no API key required)
            url = f"{JINA_READER_HOSTED_URL}/reader"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            logger.info("Using hosted Jina Reader at %s", url)
        else:
            # Use custom Jina instance with API key
            jina_api_key = os.environ.get("JINA_API_KEY", "").strip()
            jina_api_base = os.environ.get("JINA_API_BASE", "").strip()
            
            if not jina_api_base:
                return {"ok": False, "error": "JINA_API_BASE not configured"}
            
            url = f"{jina_api_base.rstrip('/')}/reader"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            
            if jina_api_key:
                headers["Authorization"] = f"Bearer {jina_api_key}"
            
            logger.info("Using custom Jina Reader at %s", url)
        
        payload = {
            "query": query,
            "contexts": contexts,
            "params": params,
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            error_msg = f"Jina Reader returned status {response.status_code}: {response.text}"
            logger.error(error_msg)
            return {"ok": False, "error": error_msg}
        
        response_data = response.json()
        
        # Try to extract answer from response
        # Handle different response formats
        answer = None
        if isinstance(response_data, dict):
            answer = response_data.get("answer") or response_data.get("data") or response_data.get("content")
            if isinstance(answer, dict):
                answer = answer.get("content") or answer.get("answer") or str(answer)
        elif isinstance(response_data, str):
            answer = response_data
        
        if answer:
            return {"ok": True, "answer": str(answer)}
        else:
            # If no structured answer, return the raw response
            return {"ok": True, "answer": json.dumps(response_data)}
        
    except requests.exceptions.Timeout:
        error_msg = "Jina Reader request timed out"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}
    except requests.exceptions.RequestException as e:
        error_msg = f"Jina Reader request failed: {str(e)}"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}
    except json.JSONDecodeError as e:
        error_msg = f"Failed to parse Jina Reader response: {str(e)}"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error in Jina Reader: {str(e)}"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}


def query_index(
    query: str,
    index_name: Optional[str] = None,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Query a custom Jina search index (optional feature).
    
    This function requires JINA_API_KEY and JINA_API_BASE to be set.
    If not configured, returns a not-enabled response.
    
    Args:
        query: Search query
        index_name: Optional index name to search
        top_k: Number of results to return
    
    Returns:
        dict: {"ok": True, "results": [...]} on success,
              {"ok": False, "error": "..."} on failure
    """
    jina_api_key = os.environ.get("JINA_API_KEY", "").strip()
    jina_api_base = os.environ.get("JINA_API_BASE", "").strip()
    
    if not jina_api_key or not jina_api_base:
        return {
            "ok": False,
            "error": "Index search requires JINA_API_KEY and JINA_API_BASE to be configured"
        }
    
    try:
        url = f"{jina_api_base.rstrip('/')}/search"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {jina_api_key}",
        }
        
        payload = {
            "query": query,
            "top_k": top_k,
        }
        
        if index_name:
            payload["index"] = index_name
        
        logger.info("Querying Jina index at %s", url)
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            error_msg = f"Jina search returned status {response.status_code}: {response.text}"
            logger.error(error_msg)
            return {"ok": False, "error": error_msg}
        
        response_data = response.json()
        
        # Extract results from response
        results = response_data.get("results") or response_data.get("data") or []
        
        return {"ok": True, "results": results}
        
    except requests.exceptions.Timeout:
        error_msg = "Jina search request timed out"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}
    except requests.exceptions.RequestException as e:
        error_msg = f"Jina search request failed: {str(e)}"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error in Jina search: {str(e)}"
        logger.error(error_msg)
        return {"ok": False, "error": error_msg}


if __name__ == "__main__":
    # Basic test block
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("=" * 50)
    print("Jina Reader Integration Test")
    print("=" * 50)
    
    print(f"\nConfiguration:")
    print(f"  JINA_USE_READER env: {os.environ.get('JINA_USE_READER', 'not set')}")
    print(f"  JINA_API_KEY set: {'yes' if os.environ.get('JINA_API_KEY') else 'no'}")
    print(f"  JINA_API_BASE set: {'yes' if os.environ.get('JINA_API_BASE') else 'no'}")
    
    print(f"\nFunction results:")
    print(f"  jina_use_reader(): {jina_use_reader()}")
    print(f"  jina_enabled(): {jina_enabled()}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-query":
        test_query = sys.argv[2] if len(sys.argv) > 2 else "What is artificial intelligence?"
        print(f"\nTesting reader_qa with query: {test_query}")
        result = reader_qa(test_query)
        print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "=" * 50)
    print("Test completed")
    print("=" * 50)
