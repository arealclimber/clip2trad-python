import re

def convert_to_markdown(text):
    # Remove extra blank lines
    text = text.strip()
    
    # Split text into lines
    lines = text.splitlines()
    
    converted_lines = []
    
    for line in lines:
        # Remove leading and trailing whitespace
        line = line.strip()
        
        # Handle primary bullet points "- "
        if line.startswith('- '):
            line = line.replace('- ', '# ', 1)
            
        # Handle secondary bullet points "• ", replace with "- "
        elif '•' in line:
            # Remove leading whitespace and replace bullet point with markdown format
            line = re.sub(r'\s*•\s*', '- ', line)
            
        # Add line if it's not empty
        if line:
            converted_lines.append(line)
    
    # Join all lines with appropriate line breaks
    return '\n'.join(converted_lines)

def process_file(input_text):
    """Process input text and return markdown format"""
    return convert_to_markdown(input_text)

if __name__ == "__main__":
    # Test example
    sample_text = """  
    
• When changing from "old process (IP check after login)" to "new process (forced 2FA)", the main difference is "preventing" suspicious logins in advance, rather than relying on "post-notification" and "user self-blocking".  
• The main challenges for the backend in the new process are "2FA code generation, sending, and verification" and "managing verification status with frontend", and deciding whether to retain some features from the old process (like IP blocking) as reinforcement.  
• Key discussion points between frontend and backend include: how to smoothly complete code input on frontend, display errors and countdown, whether to keep the old IP management interface, and UI/UX and user awareness during the transition between old and new processes.  
    
    """
    
    result = process_file(sample_text)
    print("Conversion result:\n")
    print(result) 
