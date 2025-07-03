package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
	"github.com/wraith29/dashboard/pkg/module"
)

type Module struct {
}

func NewModule() module.Module {
	return Module{}
}

func (m *Module) Preview() (fyne.Widget, error) {
	return widget.NewLabel("Hello from module"), nil
}

func (m *Module) Render() (fyne.Widget, error) {
	return widget.NewButton("Hell from render", func() { println("Hi") }), nil
}

func main() {
	println("Hello World!")
}
