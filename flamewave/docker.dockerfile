FROM golang:1.22-alpine AS build
WORKDIR /fw
COPY . .
RUN go mod download
RUN go build -o /fw/dist
FROM alpine:latest
WORKDIR /fw
COPY --from=build /fw/dist .
CMD ["./dist"]