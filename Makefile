BINARY := shipmondo
VERSION ?= dev
LDFLAGS := -s -w -X main.version=$(VERSION)

# Local development build for the host platform.
build:
	go build -ldflags "$(LDFLAGS)" -o $(BINARY) .

# Cross-compile every distributable target into ./dist (mirrors CI).
dist:
	mkdir -p dist
	CGO_ENABLED=0 GOOS=darwin  GOARCH=amd64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-darwin-amd64 .
	CGO_ENABLED=0 GOOS=darwin  GOARCH=arm64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-darwin-arm64 .
	CGO_ENABLED=0 GOOS=linux   GOARCH=amd64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-linux-amd64 .
	CGO_ENABLED=0 GOOS=linux   GOARCH=arm64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-linux-arm64 .
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-windows-amd64.exe .
	CGO_ENABLED=0 GOOS=windows GOARCH=arm64 go build -trimpath -ldflags "$(LDFLAGS)" -o dist/$(BINARY)-windows-arm64.exe .

clean:
	rm -rf dist $(BINARY)

.PHONY: build dist clean
