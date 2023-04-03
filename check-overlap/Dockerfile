# Use the official Golang image as the base image
FROM golang:1.20-alpine as builder

# Set the working directory to /app
WORKDIR /app

# Copy the source code into the container
COPY . .

# Build the executable
RUN go build -o app

# Use a minimal Alpine image to create the final container
FROM alpine:3.14

# Copy the executable from the builder container to the final container
COPY --from=builder /app/app /app/app

# Set the working directory to /app
WORKDIR /app

# Expose port 8080
EXPOSE 8080

# Run the executable
CMD ["./app"]