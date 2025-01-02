import PyPDF2


class PDFContextProvider:
    def __init__(self,fpath):
        self.fpath = fpath
        self.context_text = None
    
    def get_context(self):
        if self.context_text is None:
            self.context_text = self._read_pdf()

        return self.context_text

    def _read_pdf(self):
        with open(self.fpath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        return text
    