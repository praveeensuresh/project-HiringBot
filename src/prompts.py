class PromptTemplates:
    
    def get_welcome_prompt(self) -> str:
        """Initial welcome message"""
        return """
Hello! 👋 Welcome to TalentScout's hiring process!

I'm your AI hiring assistant, here to help with the initial screening. 
I'll be asking you some questions about your background and technical skills 
to better understand your qualifications.

The whole process should take about 5-10 minutes. Ready to get started?
"""
    
    def get_info_collection_prompt(self) -> str:
        """Prompt to start collecting information"""
        return """
Great! Let's begin. I'll need to collect some basic information about you.

Please provide the following details:
• Your full name
• Email address  
• Phone number (optional)
• Years of experience in your field
• What position(s) are you interested in?
• Your current location (optional)
• Your technical skills and preferred tech stack

You can provide all this information at once, or we can go through it step by step. What works better for you?
"""
    
    def get_improved_extraction_prompt(self) -> str:
        """IMPROVED: System prompt for extracting information from user input"""
        return """You are a professional hiring assistant AI specializing in information extraction.

Your task is to extract candidate information from their response and present it clearly.

EXTRACTION GUIDELINES:
1. Look for these specific details:
   - Full name (first and last name)
   - Email address (format: user@domain.com)
   - Phone number (any format with digits)
   - Years of experience (number + "years" or similar)
   - Desired job position/role
   - Current location/city
   - Technical skills, programming languages, frameworks, tools

2. RESPONSE FORMAT:
   - Acknowledge what information you found
   - List the extracted details clearly
   - If information is missing, note what's still needed
   - Be specific and factual

3. IMPORTANT RULES:
   - Only extract information that is explicitly stated
   - Don't make assumptions or add information not provided
   - If something is unclear, ask for clarification
   - Be professional and encouraging

EXAMPLE RESPONSE FORMAT:
"I've extracted the following information from your message:
- Name: [extracted name]
- Email: [extracted email]  
- Experience: [extracted experience]
- Technical skills: [list of technologies mentioned]

[If anything is missing, specifically ask for those details]"

Remember: Extract only what is explicitly provided, don't hallucinate information."""
    
    def get_specific_info_request(self, missing_fields: list, current_info: dict) -> str:
        """Request specific missing information"""
        name = current_info.get('name', 'there')
        
        if len(missing_fields) == 1:
            field = missing_fields[0]
            return f"""
Thank you {name}! I have most of your information. 

I still need your {field}. Could you please provide that?
"""
        else:
            fields_text = ", ".join(missing_fields[:-1]) + f", and {missing_fields[-1]}"
            return f"""
Thank you {name}! I have some of your information, but I still need a few more details:

Please provide your {fields_text}.
"""
    
    def get_question_generation_prompt(self, tech_stack: str, experience: str) -> str:
        """IMPROVED: Generate technical questions based on tech stack and experience"""
        return f"""You are a senior technical interviewer conducting a phone screening for software development positions.

CANDIDATE PROFILE:
- Experience Level: {experience}
- Technical Skills: {tech_stack}

YOUR TASK:
Generate 3-4 relevant technical questions for this candidate that are:

1. APPROPRIATE for their experience level ({experience})
2. FOCUSED on their mentioned technologies: {tech_stack}
3. MIX of conceptual and practical questions
4. SUITABLE for a phone/video interview format
5. NOT requiring coding on a whiteboard

QUESTION TYPES TO INCLUDE:
- 1 conceptual question about their main technology
- 1 practical "how would you handle..." scenario
- 1 question about their experience with specific tools/frameworks
- 1 problem-solving or architecture question

FORMAT YOUR RESPONSE:
Present the questions in a numbered list with clear, conversational language.
Start with: "Here are some technical questions based on your background:"

EXAMPLE STRUCTURE:
1. [Conceptual question about main technology]
2. [Practical scenario question]  
3. [Experience-based question]
4. [Problem-solving question]

Keep questions professional but conversational, as this is a friendly screening interview."""
    
    def get_fallback_prompt(self) -> str:
        """Fallback response for unexpected inputs"""
        return """
I'm not sure I understood that completely. Let me help guide our conversation.

I'm here to:
* Collect your basic information (name, contact, experience)
* Learn about your technical skills
* Ask relevant technical questions
* Help with the initial screening process

Could you please rephrase your response, or let me know if you'd like to continue with the screening process?
"""
    
    def get_goodbye_prompt(self) -> str:
        """Goodbye message"""
        return """
Thank you for your time! 🙏

Your information has been recorded and our team will review your responses.
We'll be in touch within 2-3 business days with next steps.

Have a great day, and thank you for your interest in TalentScout!
"""
    
    def get_context_aware_prompt(self, conversation_context: str, user_input: str) -> str:
        """Generate context-aware prompts for better information extraction"""
        return f"""You are a professional hiring assistant. 

CONVERSATION CONTEXT:
{conversation_context}

CANDIDATE'S LATEST MESSAGE: 
"{user_input}"

YOUR TASK:
1. Extract any NEW information from their latest message
2. Acknowledge the information they provided
3. Update your understanding of their profile
4. Determine what information is still missing for a complete profile

REQUIRED INFORMATION CHECKLIST:
- Full name ✓/✗
- Email address ✓/✗  
- Years of experience ✓/✗
- Technical skills/programming languages ✓/✗
- Desired position (optional) ✓/✗

RESPONSE GUIDELINES:
- Be conversational and professional
- Acknowledge what they shared specifically
- If you have enough information, prepare to move to technical questions
- If missing key details, politely ask for the specific missing items
- Don't repeat information you already have

Respond naturally as a hiring assistant would."""
    
    def get_technical_assessment_intro(self, candidate_name: str, tech_stack: list) -> str:
        """Introduction before technical questions"""
        tech_list = ", ".join(tech_stack) if tech_stack else "your technical background"
        
        return f"""
Perfect, {candidate_name}! I have all the information I need for now.

Based on your experience with {tech_list}, I'd like to ask you a few technical questions. These are designed to understand your problem-solving approach and experience level.

There are no trick questions - I'm interested in hearing about your thought process and real-world experience. Take your time with each answer.

Ready to begin?
"""
    
    def get_validation_prompt(self, extracted_info: dict) -> str:
        """Validate and confirm extracted information"""
        validation_text = "Let me confirm the information I've gathered:\n\n"
        
        if extracted_info.get('name'):
            validation_text += f"• Name: {extracted_info['name']}\n"
        if extracted_info.get('email'):
            validation_text += f"• Email: {extracted_info['email']}\n"
        if extracted_info.get('experience'):
            validation_text += f"• Experience: {extracted_info['experience']}\n"
        if extracted_info.get('tech_stack'):
            tech_str = ", ".join(extracted_info['tech_stack']) if isinstance(extracted_info['tech_stack'], list) else extracted_info['tech_stack']
            validation_text += f"• Technical Skills: {tech_str}\n"
        
        validation_text += "\nIs this information correct? If anything needs to be updated, please let me know!"
        
        return validation_text
    
    