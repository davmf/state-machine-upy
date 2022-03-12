if "%1"=="" (^
    docker run -v %CD%:/src -w /src -e MICROPYPATH="/src" -it micropython/unix:latest
) else (
    docker run -v %CD%:/src --rm -w /src -e MICROPYPATH="/src" -t micropython/unix:latest micropython-dev %1
)