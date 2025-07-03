package main

import (
	"errors"
	"fmt"
	"os"
	"plugin"

	"github.com/wraith29/dashboard/pkg/module"
)

func loadModule(modName string) (module.Module, error) {
	plug, err := plugin.Open(fmt.Sprintf("lib/%s.so", modName))
	if err != nil {
		return nil, err
	}
	fmt.Printf("%+v\n", plug)

	symb, err := plug.Lookup("NewModule")
	if err != nil {
		return nil, err
	}

	mod, ok := symb.(func() module.Module)
	if !ok {
		return nil, errors.New("invalid exported symbol")
	}

	return mod(), nil
}

func main() {
	mod, err := loadModule("test")
	if err != nil {
		fmt.Printf("Failed to load module: %+v\n", err)
		os.Exit(1)
	}

	fmt.Printf("%+v\n", mod)
}
