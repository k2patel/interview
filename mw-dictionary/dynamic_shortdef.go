package main

import (
	"fmt"
	"os"

	"io/ioutil"
	"net/http"

	"github.com/Jeffail/gabs/v2"
)

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

	// Read the API response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading API response:", err)
		return
	}

	// Parse the JSON response using gabs
	jsonParsed, err := gabs.ParseJSON(body)
	if err != nil {
		fmt.Println("Error parsing API response:", err)
		return
	}

	// Extract and display the word's pronunciation
	pronunciation, ok := jsonParsed.Path("0.hwi.prs.0.mw").Data().(string)
	if !ok {
		fmt.Println("'%s':\n", word)
	} else {
		fmt.Printf("'%s':\n", pronunciation)
	}

	// Extract and display all definitions from shortdef fields
	shortdefs := jsonParsed.Path("0.shortdef").Children()
	if len(shortdefs) == 0 {
		fmt.Println("No definitions found for the word:", word)
		return
	}

	for i, shortdef := range shortdefs {
		definition, ok := shortdef.Data().(string)
		if !ok {
			fmt.Printf("%d. Definition not found\n", i+1)
		} else {
			fmt.Printf("%d. %s\n", i+1, definition)
		}
	}
}
