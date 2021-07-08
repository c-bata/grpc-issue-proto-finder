# A regression bug report of grpc's Python library.

## Problem Details

I found a bug that it raises ModuleNotFoundError by importing a protoc-generated module after upgraded `grpcio` to `1.38.1` from `1.33.2`.
An error trace is like this:

```python
# Although this program won't raise an ModuleNotFoundError on grpcio==1.33.2,
# this program will raise an ModuleNotFoundError on grpcio==1.38.1.
from foo import a_pb2_grpc

print("success")
```

```
$ pip freeze | grep grpcio
grpcio==1.33.2
grpcio-tools==1.33.2

$ python example1.py 
success
```

```
(venv) $ pip install -U grpcio grpcio-tools
(venv) $ pip freeze | grep grpcio
grpcio==1.38.1
grpcio-tools==1.38.1

(venv) $ python example1.py 
Traceback (most recent call last):
  File "/Users/a14737/sandbox/protoc-bug-report-proto-finder/example1.py", line 5, in <module>
    from foo import a_pb2_grpc
  File "/Users/a14737/sandbox/protoc-bug-report-proto-finder/foo/a_pb2_grpc.py", line 5, in <module>
    import a_pb2 as a__pb2
ModuleNotFoundError: No module named 'a_pb2'
```

This error is raised by an import lines in `a_pb2_grpc.py`, protoc-generated Python module:

```python
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import a_pb2 as a__pb2   # ModuleNotFoundError is raised here!!!
```

In `grpcio==1.33.2`, it won't raise an exception because `grpc_tools.protoc.ProtoFinder` is set on `sys.meta_path` at `import grpc`.
But ProtoFinder is not at `grpcio==1.38.1` due to the change of https://github.com/protocolbuffers/protobuf/pull/7470.  If I explicitly imports `grpc_tools.protoc` before importing `a_pb2_grpc`, ModuleNotFoundError won't be raised.

```python
# This works fine with grpcio==1.38.1 because this program explicitly imports
# "grpc_tools.protoc" so that "grpc_tools.protoc.ProtoFinder" is set in sys.meta_path.
import grpc_tools.protoc

from foo import a_pb2_grpc

print("success")
```

```
(venv) $ pip freeze | grep grpcio
grpcio==1.38.1
grpcio-tools==1.38.1

(venv) $ python example2.py 
success
```

I think this is a regression bug which introduced by https://github.com/protocolbuffers/protobuf/pull/7470,
and we need to import `grpc_tools.protoc` from the `grpc` package as in the previous version.

## Solution


## Related issues and pull requests.

* https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-772720912
* https://github.com/protocolbuffers/protobuf/pull/7470