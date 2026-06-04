import io
from pypdf import PdfReader, PdfWriter

def split_pdf(file_bytes: bytes, start_page: int, end_page: int):
    reader = PdfReader(io.BytesIO(file_bytes))
    writer = PdfWriter()

    for page in reader.pages[start_page - 1:end_page]:  # -1 because pages are 0-indexed
        writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    
    return output
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("start", type=int)
    parser.add_argument("end", type=int)
    args = parser.parse_args()
    with open(args.pdf, 'rb') as f:
        result = split_pdf(f.read(), args.start, args.end)
    with open(f"output({args.start}-{args.end}).pdf","wb") as f:
        f.write(result.read())
