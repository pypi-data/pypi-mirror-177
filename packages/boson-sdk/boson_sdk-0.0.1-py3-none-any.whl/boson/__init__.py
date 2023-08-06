import importlib.metadata

from boson.base import BaseProvider
from boson.boson_v1_pb2 import LandingPageRequest, LandingPageResponse, ConformanceRequest, ConformanceResponse, \
    CollectionsRequest, CollectionsResponse, CollectionRequest, CollectionResponse, CollectionItemsRequest, \
    CollectionItemsResponse, CollectionItemRequest, CollectionItemResponse, SearchRequest, SearchResponse
from boson.features_pb2 import CollectionMsg, FeatureMsg, FeatureCollectionMsg, LinkMsg


__version__ = importlib.metadata.version("boson-sdk")
__all__ = [
    "BaseProvider",
    "LandingPageRequest",
    "LandingPageResponse",
    "ConformanceRequest",
    "ConformanceResponse",
    "CollectionsRequest",
    "CollectionsResponse",
    "CollectionRequest",
    "CollectionResponse",
    "CollectionItemsRequest",
    "CollectionItemsResponse",
    "CollectionItemRequest",
    "CollectionItemResponse",
    "SearchRequest",
    "SearchResponse",
    "CollectionMsg",
    "FeatureMsg",
    "FeatureCollectionMsg",
    "LinkMsg"
]
