# This works fine with grpcio==1.38.1 because this program explicitly imports
# "grpc_tools.protoc" so that "grpc_tools.protoc.ProtoFinder" is set in sys.meta_path.
import grpc_tools.protoc

from foo import a_pb2_grpc

print("success")
