clean:
	rm -rf build build.zip
	rm -rf __pycache__

fetch-dependencies:
ifeq (,$(wildcard ./bin/vendor/wkhtmltopdf))
	mkdir -p bin/
	mkdir -p bin/vendor/

	echo "Installing wkhtmltopdf."
	wget -qO- https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz | tar xpJ
	cp wkhtmltox/bin/wkhtmltopdf ./bin/vendor/
	cp wkhtmltox/bin/wkhtmltopdf ./bin/
	rm -rf wkhtmltox/
endif

docker-build:
	docker-compose build

docker-run:
	docker-compose run lambda src.lambda_function.lambda_handler

build-lambda-package: clean fetch-dependencies
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	pip install -r requirements.txt -t build/lib/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build