SRC_DIR = tex-source
BUILD_DIR = build
PUB_DIR = pub
ENTRY = paper_template
OUTPUT = llm-sql-ggra

pdf: clean
	mkdir -p $(PUB_DIR) $(BUILD_DIR)
	TEXINPUTS=$(SRC_DIR): pdflatex -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(ENTRY).tex
	BIBINPUTS=$(SRC_DIR): BSTINPUTS=$(SRC_DIR): openout_any=a bibtex $(BUILD_DIR)/$(ENTRY)
	TEXINPUTS=$(SRC_DIR): pdflatex -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(ENTRY).tex
	TEXINPUTS=$(SRC_DIR): pdflatex -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(ENTRY).tex
	cp $(BUILD_DIR)/$(ENTRY).pdf $(PUB_DIR)/$(OUTPUT).pdf
	rm -rf $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR) $(PUB_DIR)

.PHONY: pdf clean
