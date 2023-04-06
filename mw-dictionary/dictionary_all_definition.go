package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

type Definition struct {
	ShortDef []string `json:"shortdef"`
}

func getDefinitions(word, apiKey string) ([]string, error) {
	url := fmt.Sprintf("https://dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s", word, apiKey)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var definitions []Definition
	err = json.NewDecoder(resp.Body).Decode(&definitions)
	if err != nil {
		return nil, err
	}

	var result []string
	for _, d := range definitions {
		result = append(result, d.ShortDef...)
	}

	return result, nil
}

func main() {
	word := "park"
	apiKey := os.Getenv("MERRIAM_WEBSTER_API_KEY")
	if apiKey == "" {
		log.Fatal("MERRIAM_WEBSTER_API_KEY environment variable not set")
	}

	definitions, err := getDefinitions(word, apiKey)
	if err != nil {
		log.Fatalf("Failed to fetch definitions for word '%s': %v", word, err)
	}

	fmt.Printf("Definitions for word '%s':\n", word)
	for i, d := range definitions {
		fmt.Printf("%d. %s\n", i+1, d)
	}
}
