package config

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/wraith29/dashboard/internal/file"
)

type config map[key]string

var cfg config
var cfgFp string
var hasChanged bool = false

func defaultCfg(cfgDir string) config {
	return config{
		K_LIBDIR: filepath.Join(cfgDir, "libs"),
	}
}

func Setup() error {
	baseCfg, err := os.UserConfigDir()
	if err != nil {
		return err
	}

	configDir := filepath.Join(baseCfg, "dashboard")
	fmt.Printf("Checking %s\n", configDir)
	if !file.Exists(configDir) {
		if err := os.MkdirAll(configDir, os.ModePerm); err != nil {
			return err
		}
	}

	cfgFp = filepath.Join(configDir, "config.json")
	fmt.Printf("Checking %s\n", cfgFp)
	if !file.Exists(cfgFp) {
		config := defaultCfg(configDir)
		fmt.Printf("Created default config: %s\n", config)

		bytes, err := json.Marshal(config)
		if err != nil {
			return err
		}

		if err := file.CreateWithContents(cfgFp, bytes); err != nil {
			return err
		}

		cfg = config
		return nil
	}

	bytes, err := os.ReadFile(cfgFp)
	if err != nil {
		return err
	}

	err = json.Unmarshal(bytes, &cfg)

	return err
}

func Save() {
	if !hasChanged {
		return
	}

	bytes, err := json.Marshal(cfg)
	if err != nil {
		panic(err)
	}

	if err := os.WriteFile(cfgFp, bytes, os.ModePerm); err != nil {
		panic(err)
	}
}

func Get(k key) string {
	return cfg[k]
}

func Set(k key, value string) {
	cfg[k] = value
}
