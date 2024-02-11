package main

import (
	"fmt"
	"os"
	"os/exec"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Missing parameter, provide file name!")
		return
	}
	fileContent, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	input := string(fileContent)
	cmnd := exec.Command("main.exe", "arg")
	//cmnd.Run() // and wait
	cmnd.Start()
	size = len(input)
	// fmt.Println(input)
	tokenarr := LexInput(input)
	for index := 0; index < len(tokenarr); index++ {
		fmt.Printf("%-20s %s\n", TokenTypeStrings[(tokenarr[index].typetoken)], tokenarr[index].contents)
	}
	// Print the output
	// fmt.Println(string(output))
}
