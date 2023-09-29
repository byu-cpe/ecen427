serve: install
	bundle exec jekyll serve --livereload

install:
	bundle install

build: install
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --ignore_empty_alt true --ignore_missing_alt true --enforce_https false --swap_urls "^\/ecen427:" --ignore_status_codes "0,200,301,302,403" ./_site

deploy:
	bundle exec jekyll build
	ssh byu-domains "rm -rf public_html/courses/ecen625/*"
	scp -r _site/* byu-domains:public_html/courses/ecen625/
