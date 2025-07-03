package module

import (
	"fmt"
	"plugin"

	"fyne.io/fyne/v2"
)

type Module interface {
	Name() string
	Preview() (fyne.Widget, error)
	Render() (fyne.Widget, error)
}

func Load(path string) (Module, error) {
	plg, err := plugin.Open(path)
	if err != nil {
		return nil, err
	}

	sym, err := plg.Lookup("Module")
	if err != nil {
		return nil, err
	}

	mod, ok := sym.(Module)
	if !ok {
		return nil, fmt.Errorf("failed to load module from %s", path)
	}

	return mod, nil

}
