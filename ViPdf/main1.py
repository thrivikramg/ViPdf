import fitz  # PyMuPDF
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')  # Download NLTK tokenizer data

def extract_sections(pdf_path):
    sections = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            text = page.get_text()
            blocks = page.get_text("blocks")
            for b in blocks:
                block_text = b[4]  # extracting all texts
                font_size = b[0]  # Font size
                try:
                    font_weight = b[3]["font"].split(",")[1].strip()  # Font weight
                except (IndexError, TypeError):              
                    font_weight = None#if font weight is not according to logic
                if font_size > 12 and font_weight == "bold": #gets the bold from b[3]
                    sections.append(block_text)
            
            if len(sections) > 0:
                sections.append(text.split(sections[-1])[-1])
            else:
                sections.append(text)
    print("page number is :",page_num)
    return sections

def summarize_text(text, sentences_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text


pdf_path = input("Enter the PDF file path: ")
sections = extract_sections(pdf_path)

for i, section in enumerate(sections, 1):
    print(f"Section {i}:")
    print(section)
    print("Summary:")
    section_summary = summarize_text(section)
    print(section_summary)
    print()
