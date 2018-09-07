clean:
	find . -name '*.pyc' -delete
	rm -rf '__pycache__'
	rm -rf .cache
	rm -rf .tmontmp
	rm -rf .coverage
	rm -rf .testmondata
	rm -rf cov.xml

setup:
	pip install -r requirements.txt

test:
	pytest --cov=. --cov-report xml:cov.xml  --cov-report term-missing

lint:
	pylint *.py

publish: test
	python publish.py 

help:
	@echo "COMMANDS:"
	@echo "  clean          Remove all generated files."
	@echo "  setup          Setup development environment."
	@echo "  test           Run tests."
	@echo "  lint           Run analysis tools."
	@echo "  publish        Tag and push to github and update the brew formula with the new url and sha256 and push to github"
