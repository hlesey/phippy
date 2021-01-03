FROM golang:latest as builder 

WORKDIR /go/src/proxy
COPY . .
RUN go build 

FROM golang:latest 

WORKDIR /app
COPY --from=builder /go/src/proxy/proxy /app
RUN chmod 500 /app/proxy

EXPOSE 8080
CMD [ "/app/proxy" ]