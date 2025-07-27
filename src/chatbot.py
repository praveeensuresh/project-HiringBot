import ollama
import os
import json
import re
from typing import Dict, List, Optional
from prompts import PromptTemplates

class HiringAssistant:
    def __init__(self):
        """Initialize the hiring assistant with Ollama local LLM."""
        # Initialize prompts and conversation state
        self.prompts = PromptTemplates()
        self.conversation_state = "greeting"
        self.candidate_info = {
            'name': None,
            'email': None, 
            'phone': None,
            'experience': None,
            'position': None,
            'location': None,
            'tech_stack': []
        }
        self.conversation_history = []
        
        # Initialize Ollama model
        try:
            result = ollama.list()
            print("DEBUG ollama.list() result:", result, type(result))
            
            # Handle ollama._types.ListResponse object properly
            if hasattr(result, 'models'):
                models = result.models
            else:
                models = []
            
            if not models:
                self.model_name = 'llama3.2:1b'
                print("⚠️ No models detected, using fallback: llama3.2:1b")
            else:
                # Look for preferred models
                preferred = None
                for m in models:
                    if hasattr(m, 'model') and m.model.startswith('llama3.2'):
                        preferred = m
                        break
                
                if preferred:
                    self.model_name = preferred.model
                else:
                    if hasattr(models[0], 'model'):
                        self.model_name = models[0].model
                    else:
                        self.model_name = 'llama3.2:1b'
            
            self.ollama_available = True
            print(f" Ollama initialized successfully with model: {self.model_name}")
            
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            self.ollama_available = False
            self.model_name = None

    def get_welcome_message(self) -> str:
        """Return the initial welcome message."""
        return self.prompts.get_welcome_prompt()
    
    def process_message(self, user_input: str) -> str:
        """Process user input and return the assistant's response."""
        # Record user input in history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check if user wants to exit
        if self.check_exit_keywords(user_input):
            return self.prompts.get_goodbye_prompt()

        # Conversation flow with proper state management
        try:
            if self.conversation_state == "greeting":
                return self.handle_greeting_stage(user_input)
            elif self.conversation_state == "collecting_info":
                return self.handle_info_collection(user_input)
            elif self.conversation_state == "tech_questions":
                return self.handle_tech_questions(user_input)
            else:
                return self.handle_fallback(user_input)
        except Exception as e:
            print(f"Error in process_message: {e}")
            return "I apologize, but I encountered an issue processing your response. Could you please try again?"
    
    def check_exit_keywords(self, user_input: str) -> bool:
        """Detect exit keywords in user input."""
        exit_words = ["goodbye", "bye", "exit", "quit", "end", "stop"]
        return any(word in user_input.lower() for word in exit_words)
    
    def handle_greeting_stage(self, user_input: str) -> str:
        """Handle greeting and transition to info collection."""
        self.conversation_state = "collecting_info"
        return self.prompts.get_info_collection_prompt()
    
    def handle_info_collection(self, user_input: str) -> str:
        """FIXED: Extract and acknowledge candidate information properly."""
        if not self.ollama_available:
            return "Sorry, the local AI model is not available. Please ensure Ollama is installed and running."
        
        try:
            # Extract information using improved prompt
            extraction_response = self.extract_candidate_information(user_input)
            
            # Parse the extracted information
            new_info = self.parse_extraction_response(extraction_response)
            
            # Update candidate information
            self.update_candidate_info(new_info)
            
            # Check if we have sufficient information to proceed
            if self.has_sufficient_info():
                self.conversation_state = "tech_questions"
                return self.generate_acknowledgment_and_questions()
            else:
                # Ask for missing information specifically
                missing_fields = self.get_missing_fields()
                return self.prompts.get_specific_info_request(missing_fields, self.candidate_info)
        
        except Exception as e:
            print(f"Error in handle_info_collection: {e}")
            return "I had trouble processing that information. Could you please provide your details again?"
    
    def extract_candidate_information(self, user_input: str) -> str:
        """Extract information using improved prompting."""
        system_prompt = self.prompts.get_improved_extraction_prompt()
        full_prompt = f"""{system_prompt}

Current conversation context:
{self.build_conversation_context()}

Latest user message: "{user_input}"

Please extract any new information and return a structured response."""

        response = ollama.chat(
            model=self.model_name,
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=False,
            options={
                "temperature": 0.2,  # Lower temperature for more consistent extraction
                "num_predict": 400
            }
        )
        
        # Extract content from response properly
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content
        elif isinstance(response, dict):
            return response.get('message', {}).get('content', '')
        else:
            return "Could not extract information."
    
    def parse_extraction_response(self, response: str) -> Dict:
        """Parse the LLM's extraction response into structured data."""
        # Simple regex-based parsing for common patterns
        extracted_info = {}
        
        # Extract name
        name_match = re.search(r'name[:\s]+([A-Za-z\s]+)', response, re.IGNORECASE)
        if name_match:
            extracted_info['name'] = name_match.group(1).strip()
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', response)
        if email_match:
            extracted_info['email'] = email_match.group(0)
        
        # Extract phone
        phone_match = re.search(r'phone[:\s]*([\d\-\(\)\s]+)', response, re.IGNORECASE)
        if phone_match:
            extracted_info['phone'] = phone_match.group(1).strip()
        
        # Extract experience
        exp_match = re.search(r'(\d+)\s*year[s]?\s*(?:of\s*)?experience', response, re.IGNORECASE)
        if exp_match:
            extracted_info['experience'] = exp_match.group(1) + " years"
        
        # Extract tech stack
        tech_keywords = ['python', 'django', 'react', 'postgresql', 'javascript', 'node', 'sql', 'mongodb', 'flask', 'vue', 'angular']
        found_tech = []
        for tech in tech_keywords:
            if tech.lower() in response.lower():
                found_tech.append(tech.title())
        if found_tech:
            extracted_info['tech_stack'] = found_tech
        
        return extracted_info
    
    def update_candidate_info(self, new_info: Dict):
        """Update candidate information with new extracted data."""
        for key, value in new_info.items():
            if value and key in self.candidate_info:
                if key == 'tech_stack':
                    # Merge tech stacks
                    existing_tech = self.candidate_info.get('tech_stack', [])
                    combined_tech = list(set(existing_tech + value))
                    self.candidate_info['tech_stack'] = combined_tech
                else:
                    self.candidate_info[key] = value
    
    def has_sufficient_info(self) -> bool:
        """FIXED: Better logic for determining information completeness."""
        required_fields = ['name', 'email', 'experience', 'tech_stack']
        
        # Check if we have the minimum required information
        has_name = bool(self.candidate_info.get('name'))
        has_email = bool(self.candidate_info.get('email'))
        has_experience = bool(self.candidate_info.get('experience'))
        has_tech_stack = bool(self.candidate_info.get('tech_stack'))
        
        # Need at least 3 out of 4 key fields, with tech_stack being mandatory for questions
        filled_count = sum([has_name, has_email, has_experience, has_tech_stack])
        
        return filled_count >= 3 and has_tech_stack
    
    def get_missing_fields(self) -> List[str]:
        """Get list of missing required fields."""
        missing = []
        
        if not self.candidate_info.get('name'):
            missing.append('full name')
        if not self.candidate_info.get('email'):
            missing.append('email address')
        if not self.candidate_info.get('experience'):
            missing.append('years of experience')
        if not self.candidate_info.get('tech_stack'):
            missing.append('technical skills/programming languages')
        
        return missing
    
    def generate_acknowledgment_and_questions(self) -> str:
        """Generate personalized acknowledgment and transition to technical questions."""
        try:
            # Create acknowledgment
            acknowledgment = self.create_personalized_acknowledgment()
            
            # Generate technical questions
            tech_questions = self.generate_tech_questions()
            
            # Combine acknowledgment and questions
            full_response = f"{acknowledgment}\n\n{tech_questions}"
            
            # Add to conversation history
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            return full_response
        
        except Exception as e:
            print(f"Error generating acknowledgment and questions: {e}")
            return "Thank you for the information! Let me prepare some technical questions for you."
    
    def create_personalized_acknowledgment(self) -> str:
        """Create a personalized acknowledgment based on collected info."""
        name = self.candidate_info.get('name', 'there')
        experience = self.candidate_info.get('experience', 'your experience')
        tech_stack = self.candidate_info.get('tech_stack', [])
        
        acknowledgment = f"Thank you, {name}! I've recorded your information:\n\n"
        
        if self.candidate_info.get('email'):
            acknowledgment += f"✓ Email: {self.candidate_info['email']}\n"
        if experience:
            acknowledgment += f"✓ Experience: {experience}\n"
        if tech_stack:
            acknowledgment += f"✓ Technical Skills: {', '.join(tech_stack)}\n"
        
        acknowledgment += f"\nBased on your background in {', '.join(tech_stack[:3]) if tech_stack else 'software development'}, I've prepared some relevant technical questions for you."
        
        return acknowledgment
    
    def generate_tech_questions(self) -> str:
        """Generate technical questions based on candidate's tech stack."""
        tech_stack = self.candidate_info.get('tech_stack', [])
        experience = self.candidate_info.get('experience', '5 years')
        
        system_prompt = self.prompts.get_question_generation_prompt(
            tech_stack=', '.join(tech_stack),
            experience=experience
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate 3-4 technical questions for a candidate with {experience} experience in {', '.join(tech_stack)}."}
                ],
                stream=False,
                options={
                    "temperature": 0.7,
                    "num_predict": 500
                }
            )
            
            # Extract content properly
            if hasattr(response, 'message') and hasattr(response.message, 'content'):
                questions = response.message.content
            elif isinstance(response, dict):
                questions = response.get('message', {}).get('content', 'Could not generate questions.')
            else:
                questions = "Could not generate questions at this time."
                
            return questions
            
        except Exception as e:
            print(f"Error in generate_tech_questions: {e}")
            return "I'll prepare some technical questions based on your experience with Python, Django, and React. Please tell me about a challenging project you've worked on."
    
    def build_conversation_context(self) -> str:
        """Build context from conversation history."""
        context_parts = []
        
        # Add information we've already collected
        for key, value in self.candidate_info.items():
            if value:
                if key == 'tech_stack' and isinstance(value, list):
                    context_parts.append(f"{key}: {', '.join(value)}")
                else:
                    context_parts.append(f"{key}: {value}")
        
        return "Information collected so far: " + "; ".join(context_parts) if context_parts else "No information collected yet."
    
    def handle_tech_questions(self, user_input: str) -> str:
        """Handle responses to technical questions."""
        return "Thank you for your detailed responses! Our team will review your information and technical answers. We'll get back to you within 2-3 business days with next steps in the interview process."
    
    def handle_fallback(self, user_input: str) -> str:
        """Fallback response for unexpected inputs."""
        return self.prompts.get_fallback_prompt()