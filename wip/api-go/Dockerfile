FROM golang:latest as builder 

WORKDIR /go/src/phippy-api
COPY . .
RUN go build 

FROM golang:latest 

WORKDIR /app
COPY --from=builder /go/src/phippy-api/phippy-api /app
RUN chmod 500 /app/phippy-api

EXPOSE 8080
CMD [ "/app/phippy-api" ]