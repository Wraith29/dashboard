package module

import "fyne.io/fyne/v2"

type Module interface {
	Preview() (fyne.Widget, error)
	Render() (fyne.Widget, error)
}
