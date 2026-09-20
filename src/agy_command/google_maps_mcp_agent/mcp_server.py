"""Google Maps Model Context Protocol (MCP) Server.

Provides tools for Google Maps Places, Geocoding, Place Details, and Distance Matrix.
Reads GOOGLE_MAPS_API_KEY from environment variables (.env file).
"""
import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging to stderr (stdio stdout is reserved for JSON-RPC messages)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("GoogleMapsMCPServer")


class GoogleMapsService:
    """Service wrapper for Google Maps Platform REST APIs."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY", "")

    def is_configured(self) -> bool:
        """Checks if a valid Google Maps API Key is configured."""
        return bool(self.api_key and not self.api_key.startswith("YOUR_"))

    def search_places(self, query: str, location: Optional[str] = None, radius: Optional[int] = None) -> Dict[str, Any]:
        """Searches for places using Google Places Text Search API.

        Args:
            query: The search term (e.g. 'restaurants in Gangnam', 'Google Tokyo office').
            location: Optional latitude,longitude string (e.g. '37.4979,127.0276').
            radius: Optional search radius in meters.

        Returns:
            Dict containing search results, places list, and status.
        """
        if not self.is_configured():
            return {
                "status": "API_KEY_REQUIRED",
                "message": (
                    "GOOGLE_MAPS_API_KEY is not configured or using placeholder value. "
                    "Please add your key to .env file (GOOGLE_MAPS_API_KEY=AIzaSy...)."
                ),
                "query": query,
                "results": [
                    {
                        "name": f"Sample Place for '{query}'",
                        "formatted_address": "Gangnam-daero, Gangnam-gu, Seoul, South Korea",
                        "geometry": {"location": {"lat": 37.4979, "lng": 127.0276}},
                        "rating": 4.8,
                        "user_ratings_total": 1250,
                        "maps_url": f"https://www.google.com/maps/search/?api=1&query={query.replace(' ', '+')}",
                        "note": "[Mock Data] Set GOOGLE_MAPS_API_KEY in .env for live Google Maps results."
                    }
                ]
            }

        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params: Dict[str, Any] = {
            "query": query,
            "key": self.api_key,
        }
        if location:
            params["location"] = location
        if radius:
            params["radius"] = radius

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("results", [])[:10]:
                place_id = item.get("place_id", "")
                results.append({
                    "place_id": place_id,
                    "name": item.get("name"),
                    "formatted_address": item.get("formatted_address"),
                    "rating": item.get("rating"),
                    "user_ratings_total": item.get("user_ratings_total"),
                    "types": item.get("types", []),
                    "geometry": item.get("geometry", {}),
                    "maps_url": f"https://www.google.com/maps/search/?api=1&query_place_id={place_id}" if place_id else f"https://www.google.com/maps/search/?api=1&query={item.get('name')}"
                })

            return {
                "status": data.get("status", "OK"),
                "query": query,
                "total_results": len(results),
                "results": results
            }
        except requests.RequestException as e:
            logger.error("Google Places API request failed: %s", e)
            raise RuntimeError(f"Google Places API request failed: {e}") from e

    def geocode(self, address: str) -> Dict[str, Any]:
        """Geocodes an address or location name into geographic coordinates.

        Args:
            address: The address or place name to geocode.

        Returns:
            Dict containing geocoded location, coordinates, and formatted address.
        """
        if not self.is_configured():
            return {
                "status": "API_KEY_REQUIRED",
                "message": "GOOGLE_MAPS_API_KEY not configured. Showing sample geocode.",
                "address": address,
                "results": [
                    {
                        "formatted_address": f"{address}, South Korea",
                        "location": {"lat": 37.5665, "lng": 126.9780},
                        "location_type": "APPROXIMATE"
                    }
                ],
                "note": "[Mock Data] Set GOOGLE_MAPS_API_KEY in .env for live Geocoding."
            }

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": address, "key": self.api_key}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("results", []):
                results.append({
                    "formatted_address": item.get("formatted_address"),
                    "place_id": item.get("place_id"),
                    "location": item.get("geometry", {}).get("location", {}),
                    "location_type": item.get("geometry", {}).get("location_type"),
                    "address_components": item.get("address_components", [])
                })

            return {
                "status": data.get("status", "OK"),
                "results": results
            }
        except requests.RequestException as e:
            logger.error("Google Geocoding API request failed: %s", e)
            raise RuntimeError(f"Google Geocoding API request failed: {e}") from e

    def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """Retrieves detailed information about a specific place by place_id.

        Args:
            place_id: The unique Google Place ID.

        Returns:
            Dict containing phone, website, opening hours, reviews, and details.
        """
        if not self.is_configured():
            return {
                "status": "API_KEY_REQUIRED",
                "place_id": place_id,
                "name": "Sample Place Details",
                "formatted_phone_number": "+82 2-1234-5678",
                "website": "https://maps.google.com",
                "opening_hours": {"open_now": True, "weekday_text": ["Monday: 09:00 - 22:00"]},
                "note": "[Mock Data] Set GOOGLE_MAPS_API_KEY in .env for live Place Details."
            }

        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,opening_hours,reviews,url",
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "status": data.get("status", "OK"),
                "result": data.get("result", {})
            }
        except requests.RequestException as e:
            logger.error("Google Place Details API request failed: %s", e)
            raise RuntimeError(f"Google Place Details API request failed: {e}") from e

    def get_distance_matrix(self, origins: str, destinations: str, mode: str = "driving") -> Dict[str, Any]:
        """Calculates travel distance and time duration between origins and destinations.

        Args:
            origins: Starting point address or coordinates.
            destinations: Destination address or coordinates.
            mode: Travel mode ('driving', 'walking', 'bicycling', 'transit').

        Returns:
            Dict containing distance, duration, and status.
        """
        if not self.is_configured():
            return {
                "status": "API_KEY_REQUIRED",
                "origin": origins,
                "destination": destinations,
                "mode": mode,
                "distance": {"text": "12.5 km", "value": 12500},
                "duration": {"text": "25 mins", "value": 1500},
                "note": "[Mock Data] Set GOOGLE_MAPS_API_KEY in .env for live Distance Matrix."
            }

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origins,
            "destinations": destinations,
            "mode": mode,
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "status": data.get("status", "OK"),
                "origin_addresses": data.get("origin_addresses", []),
                "destination_addresses": data.get("destination_addresses", []),
                "rows": data.get("rows", [])
            }
        except requests.RequestException as e:
            logger.error("Google Distance Matrix API request failed: %s", e)
            raise RuntimeError(f"Google Distance Matrix API request failed: {e}") from e


# MCP Tool Definitions Metadata
MCP_TOOLS = [
    {
        "name": "maps_search_places",
        "description": "Searches for places, businesses, restaurants, landmarks, or addresses on Google Maps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query (e.g., 'Italian restaurant in Gangnam', 'Googleplex Mountain View')."
                },
                "location": {
                    "type": "string",
                    "description": "Optional latitude,longitude coordinate string (e.g. '37.5665,126.9780') to bias results."
                },
                "radius": {
                    "type": "integer",
                    "description": "Optional search radius around location in meters (e.g. 5000 for 5km)."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "maps_geocode",
        "description": "Converts a human-readable address or place name into geographic coordinates (lat/lng) and standardized address.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "address": {
                    "type": "string",
                    "description": "The address or place name to geocode (e.g. '1600 Amphitheatre Pkwy, Mountain View, CA')."
                }
            },
            "required": ["address"]
        }
    },
    {
        "name": "maps_place_details",
        "description": "Retrieves comprehensive details for a specific place including phone number, opening hours, website, rating, and user reviews.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "place_id": {
                    "type": "string",
                    "description": "The unique Google Place ID obtained from a previous search."
                }
            },
            "required": ["place_id"]
        }
    },
    {
        "name": "maps_distance_matrix",
        "description": "Calculates travel distance and estimated duration between origin and destination locations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "origins": {
                    "type": "string",
                    "description": "Starting address or coordinates (e.g. 'Seoul Station')."
                },
                "destinations": {
                    "type": "string",
                    "description": "Destination address or coordinates (e.g. 'Incheon International Airport')."
                },
                "mode": {
                    "type": "string",
                    "enum": ["driving", "walking", "bicycling", "transit"],
                    "default": "driving",
                    "description": "Mode of transportation (driving, walking, bicycling, transit)."
                }
            },
            "required": ["origins", "destinations"]
        }
    }
]


def handle_json_rpc(request: Dict[str, Any], maps_service: GoogleMapsService) -> Optional[Dict[str, Any]]:
    """Handles standard MCP JSON-RPC 2.0 messages."""
    msg_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    logger.info("Handling MCP method: %s (id: %s)", method, msg_id)

    # 1. Initialize Handshake
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False}
                },
                "serverInfo": {
                    "name": "google-maps-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    # 2. Initialized Notification
    if method == "notifications/initialized":
        return None

    # 3. List Tools
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": MCP_TOOLS
            }
        }

    # 4. Call Tool
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "maps_search_places":
                query = arguments.get("query", "")
                location = arguments.get("location")
                radius = arguments.get("radius")
                data = maps_service.search_places(query=query, location=location, radius=radius)
            elif tool_name == "maps_geocode":
                address = arguments.get("address", "")
                data = maps_service.geocode(address=address)
            elif tool_name == "maps_place_details":
                place_id = arguments.get("place_id", "")
                data = maps_service.get_place_details(place_id=place_id)
            elif tool_name == "maps_distance_matrix":
                origins = arguments.get("origins", "")
                destinations = arguments.get("destinations", "")
                mode = arguments.get("mode", "driving")
                data = maps_service.get_distance_matrix(origins=origins, destinations=destinations, mode=mode)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: Unknown tool '{tool_name}'"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(data, ensure_ascii=False, indent=2)
                        }
                    ],
                    "isError": False
                }
            }
        except Exception as e:
            logger.error("Error executing tool '%s': %s", tool_name, e)
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error executing tool '{tool_name}': {str(e)}"
                        }
                    ],
                    "isError": True
                }
            }

    # 5. Ping
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    # Default unrecognized method
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {
            "code": -32601,
            "message": f"Method '{method}' not implemented."
        }
    }


def run_stdio_server():
    """Main stdio loop for the MCP server."""
    maps_service = GoogleMapsService()
    logger.info("Google Maps MCP Server started on stdio.")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_json_rpc(request, maps_service)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
