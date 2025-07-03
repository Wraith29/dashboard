package ui

import (
	"fmt"
	"io/fs"
	"path/filepath"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"github.com/wraith29/dashboard/internal/config"
	"github.com/wraith29/dashboard/pkg/module"
)

type Ui struct {
	app fyne.App
	win fyne.Window
}

func New() Ui {
	a := app.New()
	win := a.NewWindow("Dashboard")

	return Ui{
		app: a,
		win: win,
	}
}

func (u *Ui) Run() error {
	modules := make([]module.Module, 0)
	modulePath := config.Get(config.K_LIBDIR)

	if err := filepath.Walk(modulePath, func(path string, info fs.FileInfo, err error) error {
		if info.IsDir() {
			return nil
		}

		mod, modErr := module.Load(path)
		if modErr != nil {
			return modErr
		}

		modules = append(modules, mod)
		return nil
	}); err != nil {
		return err
	}

	fmt.Printf("%+v\n", modules)

	modGrid := container.NewAdaptiveGrid(2)

	for _, mod := range modules {
		preview, err := mod.Preview()
		if err != nil {
			return err
		}

		modGrid.Add(preview)
	}

	u.win.SetContent(modGrid)

	u.win.Resize(fyne.NewSize(1920, 1080))
	u.win.ShowAndRun()
	return nil
}
