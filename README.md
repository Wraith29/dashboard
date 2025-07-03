# Dashboard

## Attempt using Go Plugins

### Building a plugin

```sh
go build -buildmode=plugin my_plugin.go
```

### Loading a plugin

```go
// Ignoring errors for now
plug, err := plugin.Open("./path/to/plugin.so")
symb, err := plug.Lookup("MyExportedSymbol")

callable := symb.(func() string)

fmt.Printf("Called function: %s\n", callable())
```
