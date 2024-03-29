package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
)

type APIResponse struct {
	Hwi struct {
		Prs []struct {
			Mw string `json:"mw"`
		} `json:"prs"`
	} `json:"hwi"`
	Fl       string   `json:"fl"`
	Shortdef []string `json:"shortdef"`
}

func main() {
	// Get the API key from environment variable
	apiKey := os.Getenv("MERRIAM_WEBSTER_API_KEY")
	if apiKey == "" {
		fmt.Println("Error: Merriam-Webster API key not found. Please set the MERRIAM_WEBSTER_API_KEY environment variable.")
		return
	}

	// Get the word from command line argument
	if len(os.Args) < 2 {
		fmt.Println("Error: Word argument not provided. Please provide a word as argument.")
		return
	}
	word := os.Args[1]

	// Make API request to Merriam-Webster API
	url := fmt.Sprintf("https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s", word, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("Error making API request:", err)
		return
	}
	defer resp.Body.Close()

	// Decode the API response JSON
	var apiResponse []APIResponse
	err = json.NewDecoder(resp.Body).Decode(&apiResponse)
	if err != nil {
		fmt.Println("Error decoding API response:", err)
		return
	}

	// Extract and display the word's pronunciation and part of speech
	if len(apiResponse) == 0 {
		fmt.Println("No results found for the word:", word)
		return
	}
	wordInfo := apiResponse[0]
	if wordInfo.Fl == "" {
		fmt.Println("Part of speech not found for the word:", word)
	} else {
		partOfSpeech := wordInfo.Fl
		fmt.Printf("'%s':\n", strings.Replace(wordInfo.Hwi.Prs[0].Mw, "{noun}", "", -1))
		fmt.Printf("('%s')\n", partOfSpeech)
	}

	// Extract and display all definitions from shortdef fields
	shortdefs := wordInfo.Shortdef
	if len(shortdefs) == 0 {
		fmt.Println("No definitions found for the word:", word)
		return
	}

	for i, shortdef := range shortdefs {
		fmt.Printf("%d. %s\n", i+1, shortdef)
	}
}
