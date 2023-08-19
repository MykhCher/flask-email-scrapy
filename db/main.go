package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Item struct {
	URL   string `json:"URL"`
	Email string `json:"Email"`
}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/insert", insertHandler).Methods("POST")

	http.Handle("/", r)
	http.ListenAndServe(":8081", nil)
}

func insertHandler(w http.ResponseWriter, r *http.Request) {
	var item Item
	if err := json.NewDecoder(r.Body).Decode(&item); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Connect to MongoDB client.
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	client, err := mongo.Connect(r.Context(), clientOptions)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer client.Disconnect(r.Context())

	// Get a collection from database, insert given value
	collection := client.Database("scrap_url").Collection("scraped_data")
	insertResult, err := collection.InsertOne(r.Context(), bson.M{"URL": item.URL, "Email": item.Email})
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "Inserted ID: %s", insertResult.InsertedID)
}