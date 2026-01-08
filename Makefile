serve: install
	bundle exec jekyll serve --livereload --host localhost

install:
	bundle install

build: install
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --ignore-empty-alt --ignore-missing-alt --no-enforce-https --swap_urls "^\/ecen427:" --ignore-status-codes "0,200,301,302,403" ./_site
