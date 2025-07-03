package file

import (
	"errors"
	"fmt"
	"io/fs"
	"os"
)

func Exists(fp string) bool {
	_, err := os.Stat(fp)
	if err != nil && errors.Is(err, fs.ErrNotExist) {
		return false
	} else if err != nil {
		panic(err)
	}

	return true
}

func CreateWithContents(fp string, contents []byte) error {
	fmt.Printf("Creating file %s\n", fp)
	file, err := os.OpenFile(fp, os.O_CREATE|os.O_WRONLY, os.ModePerm)
	if err != nil {
		return err
	}
	defer func() {
		if err := file.Close(); err != nil {
			panic(err)
		}
	}()

	_, err = file.Write(contents)
	return err
}
