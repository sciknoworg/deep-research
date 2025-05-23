# test_textsplitter.py

from textsplitter import RecursiveCharacterTextSplitter

def main():
    long_text = (
        "This is the first sentence. "
        "Here comes another sentence. "
        "This text continues to simulate a longer document. "
        "We are adding more content to ensure it exceeds the chunk size. "
        "Once again, this is a sentence. "
        "And another. And another.\n\n"
        "Now a new paragraph starts. This one also contains several sentences. "
        "We want to check how well the RecursiveCharacterTextSplitter handles this!"
    )

    # Create splitter with small chunk size to force multiple chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)

    chunks = splitter.split_text(long_text)

    print(f"\nGenerated {len(chunks)} chunks:\n")
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i + 1} ({len(chunk)} chars) ---")
        print(chunk)
        print()

if __name__ == "__main__":
    main()
