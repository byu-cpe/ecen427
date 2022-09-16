build:
	bundle exec jekyll build

check_links: build
	bundle exec htmlproofer --ignore_empty_alt true --ignore_missing_alt true --enforce_https false --swap_urls "^\/ecen427:" --ignore_status_codes "0,301,302,403" ./_site

serve:
	bundle exec jekyll serve

deploy:
	bundle exec jekyll build
	ssh byu-domains "rm -rf public_html/courses/ecen625/*"
	scp -r _site/* byu-domains:public_html/courses/ecen625/

develop_docker:
	docker run --rm --volume="$$PWD:/srv/jekyll" -p 4000:4000 -p 35729:35729 -it jekyll/jekyll:4.0 jekyll serve --livereload

build_docker:
	docker run --rm --volume="$$PWD:/srv/jekyll" -it jekyll/jekyll:4.0 jekyll build
