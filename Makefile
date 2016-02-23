ifndef PREFIX
  PREFIX=/usr/local
endif

install:
	install -Dm755 rofi-pass $(DESTDIR)$(PREFIX)/bin/rofi-pass
	install -Dm755 addpass $(DESTDIR)$(PREFIX)/bin/addpass
	install -Dm644 config.example $(DESTDIR)$(PREFIX)/share/doc/rofi-pass/config.example
	install -Dm644 README.md $(DESTDIR)$(PREFIX)/share/doc/rofi-pass/README.md
	install -Dm644 config.example $(DESTDIR)/etc/rofi-pass.conf
