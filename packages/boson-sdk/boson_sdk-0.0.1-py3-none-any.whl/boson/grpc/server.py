
import os
import logging
import grpc
from types import FunctionType
from typing import Optional
import numpy as np
from concurrent import futures

from boson import BaseProvider
from boson.grpc.boson_v1_pb2_grpc import BosonProviderV1Servicer, add_BosonProviderV1Servicer_to_server
from boson.boson_v1_pb2 import LandingPageRequest, LandingPageResponse, ConformanceRequest, ConformanceResponse, \
    CollectionsRequest, CollectionsResponse, CollectionRequest, CollectionResponse, CollectionItemsRequest, \
    CollectionItemsResponse, CollectionItemRequest, CollectionItemResponse, SearchRequest, SearchResponse, \
    WarpRequest, RasterResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

__all__ = ['serve']


class BosonProviderServicer(BosonProviderV1Servicer, BaseProvider):

    def LandingPage(self, request: LandingPageRequest, context: grpc.ServicerContext) -> LandingPageResponse:
        return self.landing_page(request)

    def Conformance(self, request: ConformanceRequest, context: grpc.ServicerContext) -> ConformanceResponse:
        return self.conformance(request)

    def Collections(self, request: CollectionsRequest, context: grpc.ServicerContext) -> CollectionsResponse:
        return self.collections(request)

    def Collection(self, request: CollectionRequest, context: grpc.ServicerContext) -> CollectionResponse:
        return self.collection(request)

    def CollectionItems(
            self, request: CollectionItemsRequest, context: grpc.ServicerContext) -> CollectionItemsResponse:
        pass

    def CollectionItem(self, request: CollectionItemRequest, context: grpc.ServicerContext) -> CollectionItemResponse:
        pass

    def Search(self, request: SearchRequest, context: grpc.ServicerContext) -> SearchResponse:
        pass

    def Warp(self, request: WarpRequest, context: grpc.ServicerContext) -> RasterResponse:
        pass


def serve(search_func: FunctionType, warp_func: FunctionType) -> grpc.Server:
    logger.info("initializing server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = BosonProviderServicer(search_func=search_func, warp_func=warp_func)
    add_BosonProviderV1Servicer_to_server(servicer, server)

    port = os.getenv('PROVIDER_PORT')
    if port is None or port == "":
        port = '8081'
    logger.info("initializing starting boson provider server on %s", f'[::]:{port}')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logger.info("server started")
    server.wait_for_termination()
