# Although this program won't raise an ImportError on grpcio==1.33.2,
# this program will raise an ImportError on grpcio==1.38.1.
#
# It is due to the changes on https://github.com/grpc/grpc/pull/24993.
from foo import a_pb2_grpc

print("success")
