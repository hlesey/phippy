package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/gorilla/mux"
)

var db DB

const (
	ver   string = "1.0"
	dbKey string = "objectCounter"
)

type version struct {
	Version string `json:"version"`
}

type health struct {
	Healthy bool `json:"healthy"`
}

type objects struct {
	ObjectCounter int `json:"objectCounter"`
}

type message struct {
	Message interface{} `json:"message"`
}

func newRouter() *mux.Router {
	log.Println("Creating a new Router")
	r := mux.NewRouter()
	r.HandleFunc("/", getIndex).Methods("GET")
	r.HandleFunc("/version", getVersion).Methods("GET")
	r.HandleFunc("/healthz", getHealthz).Methods("GET")
	r.HandleFunc("/hostname", getHostname).Methods("GET")
	r.HandleFunc("/objects", getObjects).Methods("GET")
	r.HandleFunc("/objects", postObjects).Methods("POST")
	r.HandleFunc("/objects", deleteObjects).Methods("DELETE")

	return r
}

func getIndex(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)
	json.NewEncoder(w).Encode(message{Message: "Phippy API"})
}

func getVersion(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)
	json.NewEncoder(w).Encode(version{Version: ver})
}

func getHealthz(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)

	healty := true
	err := db.healthz()
	if err != nil {
		healty = false
	}
	json.NewEncoder(w).Encode(health{Healthy: healty})
}

func getObjects(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)

	objectsNr, err := db.get(dbKey)
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}
	inc, err := strconv.Atoi(objectsNr)
	json.NewEncoder(w).Encode(objects{ObjectCounter: inc})
}

func postObjects(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)

	// get dbKey from redis
	objectsNr, err := db.get(dbKey)
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}

	// increment key +1
	inc, err := strconv.Atoi(objectsNr)
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}
	inc++
	objectsNr = strconv.Itoa(inc)

	err = db.set(dbKey, objectsNr)
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}

	json.NewEncoder(w).Encode(message{Message: "The counter was increased"})
}

func deleteObjects(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)

	err := db.set(dbKey, "0")
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}
	json.NewEncoder(w).Encode(message{Message: "The counter was reset."})
}

func getHostname(w http.ResponseWriter, r *http.Request) {
	log.Println(r.Method + r.URL.Path)

	hostname, err := os.Hostname()
	if err != nil {
		json.NewEncoder(w).Encode(message{Message: err})
		return
	}
	msg := fmt.Sprintf("Hostname=%s", hostname)
	json.NewEncoder(w).Encode(message{Message: msg})
}

func initDB() {
	log.Println("Inititilize connection to DB")

	redisHost := os.Getenv("REDIS_HOST")
	redisPort := os.Getenv("REDIS_PORT")

	if redisHost == "" || redisPort == "" {
		log.Fatal("REDIS_HOST and REDIS_PORT must be specified.")
	}

	dbAddr := redisHost + ":" + redisPort
	db = DB{}
	db.newClient(dbAddr)
	db.initKey(dbKey, "0")
}

func main() {
	log.Println("Starting the app..")
	initDB()
	r := newRouter()
	http.ListenAndServe(":8080", r)
}
