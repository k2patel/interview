package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

type definition struct {
	Dt       string   `json:"dt"`
	Fl       string   `json:"fl"`
	Shortdef []string `json:"shortdef"`
}

type pronunciation struct {
	Mw string `json:"mw"`
}

type entry struct {
	Hwi struct {
		Prs []pronunciation `json:"prs"`
	} `json:"hwi"`
	Fl string `json:"fl"`
}

func getDefinition(word string, apiKey string) (string, error) {
	url := fmt.Sprintf("https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s", word, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var definitions []definition
	err = json.NewDecoder(resp.Body).Decode(&definitions)
	if err != nil {
		return "", err
	}

	// Check if the API returned a definition
	if len(definitions) > 0 {
		definition := definitions[0]
		return definition.Shortdef[0], nil
	}

	return "", fmt.Errorf("no definition found for %s", word)
}

func formatDefinition(pronunciation string, partOfSpeech string, definition string) string {
	formattedDefinition := fmt.Sprintf("`%s`\t (%s): %s", pronunciation, partOfSpeech, definition)
	return formattedDefinition
}

func main() {

	apiKey := os.Getenv("MERRIAM_WEBSTER_API_KEY")
	if apiKey == "" {
		fmt.Fprintf(os.Stderr, "MERRIAM_WEBSTER_API_KEY environment variable not set")
		os.Exit(1)
	}

	if len(os.Args) != 2 {
		fmt.Println("Usage: go run dictionary.go <word>")
		return
	}

	word := os.Args[1]
	definition, err := getDefinition(word, apiKey)
	if err != nil {
		fmt.Println(err)
		return
	}

	url := fmt.Sprintf("https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s", word, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()

	var entries []entry
	err = json.NewDecoder(resp.Body).Decode(&entries)
	if err != nil {
		fmt.Println(err)
		return
	}

	if len(entries) > 0 {
		pronunciation := entries[0].Hwi.Prs[0].Mw
		partOfSpeech := entries[0].Fl
		formattedDefinition := formatDefinition(pronunciation, partOfSpeech, definition)
		fmt.Println(formattedDefinition)
	} else {
		fmt.Printf("No definition found for %s\n", word)
	}
}
