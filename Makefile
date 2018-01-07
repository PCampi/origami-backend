all: clean

clean:
	@echo "Cleaning"
	@if [ -d ./__pycache__ ]; then rm -r ./__pycache__ ; fi
	@if [ -d origami/__pycache__ ]; then rm -r origami/__pycache__ ; fi
	@if [ -d origami/db/__pycache__ ]; then rm -r origami/db/__pycache__ ; fi
	@if [ -d origami/middleware/__pycache__ ]; then rm -r origami/middleware/__pycache__ ; fi
	@if [ -d origami/resources/__pycache__ ]; then rm -r origami/resources/__pycache__ ; fi
	@if [ -d origami/tests/__pycache__ ]; then rm -r origami/tests/__pycache__ ; fi
	@echo "Finished cleaning"