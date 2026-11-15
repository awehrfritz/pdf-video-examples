# Example PDFs for screen annotations with media renditions.
# Uses the multimedia.sty in this directory (beamer's package plus \media).

EXAMPLES := $(basename $(wildcard 0*.tex))
SOURCES  := README.md LICENSE Makefile make-media.py make-pptx.py example-setup.tex richmedia.tex \
            multimedia.sty clip.mp4 clip2.mp4 tone.wav $(EXAMPLES:=.tex) 08-libreoffice-click.pptx
DIR      := $(notdir $(CURDIR))
ZIP      := pdf-video-examples.zip

all: $(EXAMPLES:=.pdf)

%.pdf: %.tex example-setup.tex richmedia.tex multimedia.sty clip.mp4 clip2.mp4 tone.wav
	pdflatex -interaction=nonstopmode -halt-on-error $<

clip.mp4 clip2.mp4 tone.wav: make-media.py
	uv run --no-project --with av --with numpy python make-media.py

08-libreoffice-click.pptx: make-pptx.py clip.mp4 clip2.mp4
	uv run --no-project --with python-pptx --with pillow python make-pptx.py

08-libreoffice-click.pdf: 08-libreoffice-click.pptx
	libreoffice --headless --convert-to pdf:impress_pdf_Export $<

# Sources and PDFs in a zip file, under the directory name of this directory.
zip: $(ZIP)

$(ZIP): $(SOURCES) $(EXAMPLES:=.pdf) 08-libreoffice-click.pdf
	rm -f $@
	cd .. && zip -q -X $(DIR)/$@ $(addprefix $(DIR)/,$^)

clean:
	rm -f *.aux *.log

# Removes everything that `make` and `make zip` create; keeps the media files,
# which need PyAV to regenerate.
distclean: clean
	rm -f $(EXAMPLES:=.pdf) 08-libreoffice-click.pdf 08-libreoffice-click.pptx $(ZIP)

.PHONY: all zip clean distclean
