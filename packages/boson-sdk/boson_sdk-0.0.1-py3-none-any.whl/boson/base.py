from types import FunctionType
from typing import Optional

from boson.boson_v1_pb2 import LandingPageResponse, ConformanceRequest, ConformanceResponse, \
    CollectionsRequest, CollectionsResponse, CollectionRequest, CollectionResponse, WarpRequest, RasterResponse


class BaseProvider:
    def __init__(self,
                 title: str = 'remote',
                 description: str = 'a remote Boson provider',
                 license: str = '(unknown)',
                 extent: Optional[dict] = None,
                 search_func: Optional[FunctionType] = None,
                 warp_func: Optional[FunctionType] = None) -> None:

        self.title = title
        self.description = description
        self.license = license
        self.extent = extent
        if self.extent is None:
            self.extent = {
                'spatial': {
                    'bbox': [[-180.0, -90.0, 180.0, 90.0]]
                },
                'temporal': {
                    'interval': [[None, None]]
                }
            }

        if search_func is not None and not callable(search_func):
            raise ValueError('search_func must be a callable or None')

        self.search_func = search_func

        if warp_func is not None and not callable(warp_func):
            raise ValueError('warp_func must be a callable or None')
        self.warp_func = warp_func
        super().__init__()

    def landing_page(self, LandingpageRequest) -> LandingPageResponse:
        return LandingPageResponse(
            title=self.title,
            description=self.description,
            links=[]
        )

    def conformance(self, request: ConformanceRequest) -> ConformanceResponse:
        return ConformanceResponse(
            conforms_to=[
                'https://api.stacspec.org/v1.0.0/core',
                'https://api.stacspec.org/v1.0.0/item-search',
                'https://api.stacspec.org/v1.0.0/ogcapi-features',
                'https://api.stacspec.org/v1.0.0/collections',
                'http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core',
                'http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30',
                'http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson'
            ]
        )

    def collection(self, request: CollectionRequest) -> CollectionResponse:
        return CollectionResponse(collection=self._collection())

    def collections(self, request: CollectionsRequest) -> CollectionsResponse:
        return CollectionsResponse(collections=[self._collection()])

    def _collection(self) -> dict:
        return {
            'type': 'Collection',
            'stac_version': 'v1.0.0',
            'id': self.title.tolower().replace(' ', ''),
            'title': self.title,
            'description': self.description,
            'license': self.license,
        }

    def warp(self, request: WarpRequest) -> RasterResponse:
        pass
