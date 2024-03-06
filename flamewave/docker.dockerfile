FROM golang:1.22-alpine AS build
WORKDIR /fw
COPY . .
RUN go mod download
RUN go build -o /fw/dist
EXPOSE 8080
CMD ["./dist"]