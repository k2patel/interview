BINARY_NAME = dictionary

all: build test
 
build:
	go build -o ${BINARY_NAME} dictionary.go

test:
	go test -v dictionary.go
 
run:
	go build -o ${BINARY_NAME} dictionary.go
	./${BINARY_NAME}
 
clean:
	go clean
	rm ${BINARY_NAME}
