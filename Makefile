all: audio

audio: de el en es ru th tr na

.PHONY: all audio

de: $(patsubst assets/audio/de/%.wav,colournaming/static/audio/de/%.mp3,$(wildcard assets/audio/de/*.wav))

el: $(patsubst assets/audio/el/%.wav,colournaming/static/audio/el/%.mp3,$(wildcard assets/audio/el/*.wav))

en: $(patsubst assets/audio/en/%.wav,colournaming/static/audio/en/%.mp3,$(wildcard assets/audio/en/*.wav))

es: $(patsubst assets/audio/es/%.wav,colournaming/static/audio/es/%.mp3,$(wildcard assets/audio/es/*.wav))

ru: $(patsubst assets/audio/ru/%.wav,colournaming/static/audio/ru/%.mp3,$(wildcard assets/audio/ru/*.wav))

th: $(patsubst assets/audio/th/%.wav,colournaming/static/audio/th/%.mp3,$(wildcard assets/audio/th/*.wav))

tr: $(patsubst assets/audio/tr/%.wav,colournaming/static/audio/tr/%.mp3,$(wildcard assets/audio/tr/*.wav))

na: $(patsubst assets/audio/na/%.wav,colournaming/static/audio/na/%.mp3,$(wildcard assets/audio/na/*.wav))

colournaming/static/audio/de/%.mp3: assets/audio/de/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/el/%.mp3: assets/audio/el/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/en/%.mp3: assets/audio/en/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/es/%.mp3: assets/audio/es/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/ru/%.mp3: assets/audio/ru/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/th/%.mp3: assets/audio/th/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/tr/%.mp3: assets/audio/tr/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@

colournaming/static/audio/na/%.mp3: assets/audio/na/%.wav
	mkdir -p $(dir $@)
	lame --silent --preset voice $< $@
