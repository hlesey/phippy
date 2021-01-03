package main

import (
	"log"

	"github.com/go-redis/redis"
)

//DB struct
type DB struct {
	client *redis.Client
}

func (db *DB) newClient(addr string) {
	db.client = redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	_, err := db.client.Ping().Result()
	if err != nil {
		log.Fatal(err)
	}
}

func (db DB) set(key string, value string) error {
	log.Println("Redis setting key: " + key + " and value: " + value)
	err := db.client.Set(key, value, 0).Err()
	return err
}

func (db DB) get(key string) (string, error) {
	log.Println("Redis getting key: " + key)
	val, err := db.client.Get(key).Result()
	return val, err
}

func (db DB) initKey(key string, value string) error {
	log.Println("Redis init key: " + key)
	_, err := db.client.Get(key).Result()
	if err != nil {
		err = db.set(key, value)
	}
	return err
}

func (db DB) healthz() error {
	_, err := db.client.Ping().Result()
	return err
}
