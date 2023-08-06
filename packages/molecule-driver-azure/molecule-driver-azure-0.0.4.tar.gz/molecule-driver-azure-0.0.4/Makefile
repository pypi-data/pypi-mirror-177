build:
	python -m build

install:
	pip install -e .

publish:
	twine upload -r testpypi dist/*

clean:
	rm -rf ./dist/
	rm -rf ./molecule_driver_azure.egg-info/