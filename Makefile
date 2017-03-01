install:
	bash -c '. bin/activate.sh'

test:
	bash -c '. bin/activate.sh 2>/dev/null; nose2'

lint:
	bash -c '. bin/activate.sh 2>/dev/null; pylint -r n -f colorized mbtaalerts'

freeze:
	bash -c '. bin/activate.sh; pip freeze | tee requirements.txt'

clean:
	rm -rf htmlcov
	rm -rf htmllint
	rm nose2-junit.xml

run:
	bash -c ". bin/activate.sh 2>/dev/null; python -m mbtaalerts.$(filter-out $@, $(MAKECMDGOALS))"

%:
	@:

check: lint test
