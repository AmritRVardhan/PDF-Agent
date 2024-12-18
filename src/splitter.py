def split_sections(text):
    """
    Split text into sections first by length (2048 chars) and then by version numbers.
    Returns list of lists containing the split sections.
    """
    def find_last_newline(text, max_length=2048):
        """Find last newline within max_length characters"""
        text_portion = text[:max_length]
        last_nl = text_portion.rfind('\n')
        return last_nl if last_nl != -1 else max_length

    sections = []
    while len(text) > 2048:
        # Find last newline within 2048 chars
        split_point = find_last_newline(text)
        sections.append(text[:split_point])
        text = text[split_point:].lstrip()

    # Add remaining text if any
    if text:
        sections.append(text)
        
    return sections

def use_splitter(delimiters, text):
    result = split_handbook(text, delimiters)
        # Print results

    for i, section in enumerate(result):
        print(f"\nSection {i + 1} ({len(section)} subsections):")
        for j, subsection in enumerate(section):
            print(f"  Subsection {j + 1}: {len(subsection)} characters")
            print(f"  Starts with: {subsection[:50]}...")

# Example usage:
if __name__ == "__main__":
    # Example text
    sample_text = """1.0 Introduction
This is the introduction section.
It contains multiple lines.

1.1 Background
This is the background section.
More content here.

2.0 Methods
This is the methods section.
It contains important information.

2.1 Results
These are the results.
More data here."""

    version_numbers = [1.0, 1.1, 2.0, 2.1]
    result = split_text_hierarchically(sample_text, version_numbers, max_length=100)
    
    # Print results
    for i, section in enumerate(result):
        print(f"Major Section {i + 1}:")
        for j, subsection in enumerate(section):
            print(f"  Subsection {j + 1}: {len(subsection)} characters")
            print("  Content:", subsection[:50] + "..." if len(subsection) > 50 else subsection)
        print()