# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.protobufs.keys_pairs_pb2 as keys__pairs__pb2


class KeysPairsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.keysPairs = channel.unary_unary(
                '/KeysPairsService/keysPairs',
                request_serializer=keys__pairs__pb2.EncryptKeysRequest.SerializeToString,
                response_deserializer=keys__pairs__pb2.EncryptKeysResponse.FromString,
                )


class KeysPairsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def keysPairs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KeysPairsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'keysPairs': grpc.unary_unary_rpc_method_handler(
                    servicer.keysPairs,
                    request_deserializer=keys__pairs__pb2.EncryptKeysRequest.FromString,
                    response_serializer=keys__pairs__pb2.EncryptKeysResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'KeysPairsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KeysPairsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def keysPairs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KeysPairsService/keysPairs',
            keys__pairs__pb2.EncryptKeysRequest.SerializeToString,
            keys__pairs__pb2.EncryptKeysResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
