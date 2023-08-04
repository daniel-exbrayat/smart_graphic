.PHONY: package check package all

ref_files = README.md LICENSE Makefile $(wildcard smart_*)

package_files := $(patsubst %,package/%,$(ref_files))

Smart_Graphic.run: $(package_files)
	@echo -n "[@]: $@:"
	@echo    "[^]: $^"
	-rm $@
	makeself                            \
		--lsm smart_graphic.lsm         \
		--target /tmp/smart_graphic/    \
		./package/                      \
	    $@                              \
		"SMART GRAPHIC package installer <daniel.exbrayat@laposte.net>" \
		./smart_install.sh 

package/%: %
	@echo -n "[@]: $@:"
	@echo    "[^]: $^"
	@cp -vui --target-directory=package/ $^


# package/smart_%: smart_%
# 	cp -vui --target-directory=package/ $^

# package/README.md: README.md
# 	cp -vui --target-directory=package/ $^

# package/LICENSE: LICENSE
# 	cp -vui --target-directory=package/ $^

# package: smart_graphic.run
# 	@echo "==> rule package:"
# 	@echo "@: $@"
# 	@echo "<: $<"
# 	@echo "*: $*"
# 	@echo "^: $^"

all:
	@echo "$(ref_files)"
	@echo "$(package_files)"

memo: 
	@echo "==> rule smart_graphic.run:"
	@echo "@: $@"
	@echo "<: $<"
	@echo "*: $*"
	@echo "^: $^"

#check:
#	@echo 'make check'
#	-cmp      ./smart_graphic.py    /usr/local/bin/smart_graphic.py \
#        && echo 'OK ./smart_graphic.py'                             \
#        || sdiff -s ./smart_graphic.py    /usr/local/bin/smart_graphic.py
#	-sdiff -s ./smart_logger        /etc/cron.daily/smart_logger

#package/smart_graphic.run: README LICENSE smart_*.* 
#	@echo yes

