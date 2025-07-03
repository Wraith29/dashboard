package main

import (
	"github.com/wraith29/dashboard/internal/config"
	"github.com/wraith29/dashboard/internal/ui"
)

func main() {
	if err := config.Setup(); err != nil {
		panic(err)
	}
	defer config.Save()

	app := ui.New()

	if err := app.Run(); err != nil {
		panic(err)
	}
}
