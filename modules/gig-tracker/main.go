package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/widget"
)

type module struct {
}

func (m *module) Name() string {
	return "Gig Tracker"
}

func (m *module) Preview() (fyne.Widget, error) {
	return widget.NewLabel("GT Preview"), nil
}

func (m *module) Render() (fyne.Widget, error) {
	return widget.NewLabel("GT Render"), nil
}

var Module module
