package main

import (
	"fmt"
	"net/http"
)

type helloHandler struct{}

func (h *helloHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("Sucess!"))
}

func main() {
	http.Handle("/", &helloHandler{})
	fmt.Println("Server Listen on :9999")
	http.ListenAndServe(":9999", nil)
}
