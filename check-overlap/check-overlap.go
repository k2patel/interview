package main

import (
	"encoding/json"
	"log"
	"net/http"
	"time"
)

type dateRange struct {
	Start time.Time `json:"start"`
	End   time.Time `json:"end"`
}

type overlapResponse struct {
	Overlap bool `json:"overlap"`
}

func checkOverlap(w http.ResponseWriter, r *http.Request) {
	// Parse the request body into a struct
	var requestBody struct {
		Range1 dateRange `json:"range1"`
		Range2 dateRange `json:"range2"`
	}
	err := json.NewDecoder(r.Body).Decode(&requestBody)
	if err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Check if the date ranges overlap
	overlap := !(requestBody.Range1.End.Before(requestBody.Range2.Start) || requestBody.Range2.End.Before(requestBody.Range1.Start))

	// Create the response struct and encode it to JSON
	response := overlapResponse{Overlap: overlap}
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		log.Printf("Error marshaling JSON response: %v", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	// Write the response back to the client
	w.Header().Set("Content-Type", "application/json")
	w.Write(jsonResponse)
}

func main() {
	http.HandleFunc("/check-overlap", checkOverlap)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
