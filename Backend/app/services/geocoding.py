import math
import json
import time
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from app.config import BASE_DIR

logger = logging.getLogger("civicquest.geocoding")

CACHE_FILE = BASE_DIR / "data" / "geocode_cache.json"

class GeocodingService:
    def __init__(self):
        self.file_cache: Dict[str, Dict[str, Any]] = self._load_cache()
        self.geolocator = None
        self.last_query_time = 0.0

    def _load_cache(self) -> dict:
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading geocode cache: {e}")
        return {}

    def _save_cache(self):
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.file_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving geocode cache: {e}")

    def get_geolocator(self):
        if not self.geolocator:
            self.geolocator = Nominatim(user_agent="civicquest_platform_v1", timeout=6)
        return self.geolocator

    def get_cached_coordinates(
        self,
        query_key: str,
        db: Optional[Session] = None
    ) -> Optional[Tuple[Optional[float], Optional[float], str, Optional[str]]]:
        """
        Check database LocationCache and local cache for query_key.
        Returns (lat, lng, location_source, location_accuracy) or None if not cached.
        """
        cleaned = query_key.strip().lower()
        if not cleaned:
            return None

        # 1. Check PostgreSQL LocationCache if db session provided
        if db is not None:
            try:
                from app.models import LocationCache
                cached = db.query(LocationCache).filter(LocationCache.query_key == cleaned).first()
                if cached:
                    return cached.latitude, cached.longitude, cached.location_source, cached.location_accuracy
            except Exception as e:
                logger.warning(f"Error querying LocationCache in DB: {e}")

        # 2. Check memory/file cache
        if cleaned in self.file_cache:
            entry = self.file_cache[cleaned]
            return (
                entry.get("lat"),
                entry.get("lng"),
                entry.get("source", "GEOCODED"),
                entry.get("accuracy", "APPROXIMATE")
            )

        return None

    def cache_coordinates(
        self,
        query_key: str,
        lat: Optional[float],
        lng: Optional[float],
        location_source: str,
        location_accuracy: Optional[str] = None,
        project_id: Optional[str] = None,
        db: Optional[Session] = None
    ):
        """Save resolved coordinates to PostgreSQL LocationCache and file cache."""
        cleaned = query_key.strip().lower()
        if not cleaned:
            return

        # Save to file cache
        self.file_cache[cleaned] = {
            "lat": lat,
            "lng": lng,
            "source": location_source,
            "accuracy": location_accuracy
        }
        self._save_cache()

        # Save to PostgreSQL LocationCache if db available
        if db is not None:
            try:
                from app.models import LocationCache
                existing = db.query(LocationCache).filter(LocationCache.query_key == cleaned).first()
                if existing:
                    existing.latitude = lat
                    existing.longitude = lng
                    existing.location_source = location_source
                    existing.location_accuracy = location_accuracy
                    if project_id:
                        existing.project_id = project_id
                else:
                    new_cache = LocationCache(
                        query_key=cleaned,
                        project_id=project_id,
                        latitude=lat,
                        longitude=lng,
                        location_source=location_source,
                        location_accuracy=location_accuracy
                    )
                    db.add(new_cache)
                db.commit()
            except Exception as e:
                db.rollback()
                logger.warning(f"Error writing to LocationCache in DB: {e}")

    def geocode(
        self,
        query: str,
        db: Optional[Session] = None,
        project_id: Optional[str] = None
    ) -> Tuple[Optional[float], Optional[float], str, Optional[str]]:
        """
        Geocode location string safely with persistent caching and rate limiting.
        Never repeatedly queries the same location.
        Returns: (latitude, longitude, location_source, location_accuracy)
        """
        cleaned_query = query.strip()
        if not cleaned_query:
            return None, None, "MISSING", "MISSING"

        # Check existing cache
        cached = self.get_cached_coordinates(cleaned_query, db=db)
        if cached is not None:
            return cached

        # Rate limiting: OpenStreetMap Nominatim guidelines require >= 1.0s between requests
        now = time.time()
        elapsed = now - self.last_query_time
        if elapsed < 1.1:
            time.sleep(1.1 - elapsed)

        try:
            self.last_query_time = time.time()
            locator = self.get_geolocator()
            location = locator.geocode(cleaned_query)
            if location:
                lat, lng = location.latitude, location.longitude
                source = "GEOCODED"
                accuracy = "APPROXIMATE"
                self.cache_coordinates(
                    query_key=cleaned_query,
                    lat=lat,
                    lng=lng,
                    location_source=source,
                    location_accuracy=accuracy,
                    project_id=project_id,
                    db=db
                )
                return lat, lng, source, accuracy
        except (GeocoderTimedOut, GeocoderServiceError, Exception) as e:
            logger.warning(f"Geocoding service error for '{cleaned_query}': {e}")

        # Mark as MISSING in cache to avoid repetitive failed lookups
        self.cache_coordinates(
            query_key=cleaned_query,
            lat=None,
            lng=None,
            location_source="MISSING",
            location_accuracy="MISSING",
            project_id=project_id,
            db=db
        )
        return None, None, "MISSING", "MISSING"

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate geographic distance between two coordinates in meters.
    Uses Haversine formula.
    """
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def evaluate_gps_verification(
    gps_lat: Optional[float],
    gps_lng: Optional[float],
    project_lat: Optional[float],
    project_lng: Optional[float],
    location_source: Optional[str],
    max_verified_distance_meters: float = 200.0
) -> Tuple[str, Optional[float]]:
    """
    Evaluates citizen GPS proximity relative to recorded government project coordinates.
    Enforces honest location reporting:
    - If government location is APPROXIMATE:
      GPS verification status is LIMITED (cannot prove exact work site attendance).
    - If government location is EXACT_DATASET or GEOCODED:
      Returns VERIFIED if within 200m, else UNVERIFIED.
    - If no coordinates are available:
      Returns NO_COORDINATES.
    Returns: (gps_verification_status, calculated_distance_meters)
    """
    if gps_lat is None or gps_lng is None or project_lat is None or project_lng is None:
        return "NO_COORDINATES", None

    distance = calculate_haversine_distance(gps_lat, gps_lng, project_lat, project_lng)
    norm_source = (location_source or "MISSING").upper()

    if norm_source == "APPROXIMATE":
        # Honest limitation: cannot claim exact attendance when project location is approximate
        return "LIMITED", distance
    elif norm_source in ("EXACT_DATASET", "GEOCODED"):
        if distance <= max_verified_distance_meters:
            return "VERIFIED", distance
        return "UNVERIFIED", distance
    else:
        return "LIMITED", distance

geocoding_service = GeocodingService()
