from grpc.tools import protoc

protoc.main(
    (
        "",
        "-I.",
        "--python_out=./foo/",
        "--grpc_python_out=./foo/",
        "./a.proto",
    )
)
