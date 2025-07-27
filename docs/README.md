# TalentScout Hiring Assistant Chatbot

An intelligent AI-powered hiring assistant built with Streamlit and Ollama's Llama 3.2:1b model for conducting initial candidate screenings and technical assessments.

##  Project Overview

The TalentScout Hiring Assistant is a conversational AI chatbot designed to streamline the initial stages of the hiring process. It conducts professional candidate screenings by:

- **Greeting candidates** and explaining the screening process
- **Collecting essential information** (name, email, phone, experience, desired positions, location)
- **Analyzing technical skills** from candidate responses
- **Generating personalized technical questions** based on their tech stack
- **Maintaining conversation context** throughout the interaction
- **Providing professional closure** with next steps information

### Key Features
-  **Local AI Processing**: Uses Ollama with Llama 3.2:1b for privacy-compliant, local LLM inference
-  **Natural Conversation Flow**: Maintains context and handles multi-turn conversations
-  **Dynamic Question Generation**: Creates relevant technical questions based on candidate's skills
-  **Privacy-First Design**: No data persistence, GDPR-compliant approach
-  **Web-Based Interface**: Clean, responsive Streamlit UI accessible via browser
-  **Real-time Processing**: Fast response times with local model deployment

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space for model and dependencies
- **Python**: 3.8 or higher

### Software Dependencies
- Ollama (latest version)
- Python 3.8+
- pip package manager

## Installation Instructions

### Step 1: Install Ollama
Download and install Ollama from [https://ollama.ai](https://ollama.ai)

1. Download the Windows installer
2. Run the installer with administrator privileges
3. Restart your terminal/command prompt

### Step 2: Pull the Required Model
```bash
# Pull Llama 3.2:1b model (approximately 1.3GB)
ollama pull llama3.2:1b

# Verify model installation
ollama list
```

### Step 3: Clone and Set Up the Project
```bash
# Clone the repository
git clone <your-repository-url>
cd talentscout-chatbot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Start Ollama Service
```bash
# Start Ollama server (keep this terminal open)
ollama serve
```

### Step 5: Launch the Application
```bash
# In a new terminal, with virtual environment activated
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

## Usage Guide

### Starting a Screening Session
1. Open your browser to `http://localhost:8501`
2. The chatbot will greet you with a welcome message
3. Follow the conversation flow naturally

### Providing Information
When prompted, provide your details in any format:
```
"Hi! I'm John Smith, email john@example.com, phone 555-123-4567. 
I have 5 years experience as a software developer, looking for 
Senior Python Developer positions in New York. I work with 
Python, Django, React, and PostgreSQL."
```

### Technical Questions Phase
After information collection, the bot will generate 3-5 technical questions based on your mentioned skills.

### Ending the Session
Use keywords like "goodbye", "bye", "quit", or "end" to conclude the session gracefully.

## Technical Architecture

### Technology Stack
- **Frontend**: Streamlit 1.28.0
- **Backend**: Python 3.8+
- **AI Model**: Ollama Llama 3.2:1b (1.3B parameters)
- **Environment Management**: python-dotenv
- **UI Components**: streamlit-chat


### Model Details: Llama 3.2:1b
- **Parameters**: 1.3 billion
- **Context Length**: 128,000 tokens
- **Model Size**: ~1.3GB
- **Use Cases**: Ideal for conversation, information extraction, and text generation
- **Performance**: Fast inference on consumer hardware
- **Language Support**: Primarily English, with multilingual capabilities

### Architectural Decisions

**Local LLM Deployment**: Chose Ollama over cloud APIs for:
- Data privacy compliance
- Reduced latency
- Cost-effective scaling
- Offline capability

**Streamlit Framework**: Selected for:
- Rapid prototyping
- Built-in session state management
- Simple deployment options
- Real-time chat interface capabilities

**Modular Design**: Separated concerns into distinct modules:
- `main.py`: UI layer and user interaction
- `chatbot.py`: Business logic and AI integration
- `prompts.py`: Prompt engineering and templates
- `utils.py`: Data processing and validation

## Prompt Design 

### Prompt Engineering Approach
Our prompt design follows a structured methodology optimized for Ollama's Llama 3.2:1b model:

#### 1. **Welcome Prompt**
```python
def get_welcome_prompt(self) -> str:
    return """
    Hello! 👋 Welcome to TalentScout's hiring process!
    
    I'm your AI hiring assistant, here to help with the initial screening. 
    I'll be asking you some questions about your background and technical skills 
    to better understand your qualifications.
    
    The whole process should take about 5-10 minutes. Ready to get started?
    """
```

**Design Rationale**: 
- Clear role definition
- Sets expectations for time commitment
- Professional yet friendly tone
- Call-to-action to engage user

#### 2. **Information Extraction Prompt**
```python
def get_info_extraction_prompt(self) -> str:
    return """
    You are a professional hiring assistant. Extract candidate information from their response.
    
    Look for:
    - Name
    - Email
    - Phone
    - Experience level
    - Desired positions
    - Location
    - Technical skills/tech stack
    
    If information is missing, politely ask for the missing details.
    Be professional, friendly, and encouraging.
    """
```

**Design Rationale**:
- Specific instruction format for consistent extraction
- Clear field definitions
- Maintains professional tone
- Handles incomplete information gracefully

#### 3. **Technical Question Generation Prompt**
```python
def get_question_generation_prompt(self, tech_stack: str) -> str:
    return f"""
    You are a technical interviewer for TalentScout recruitment agency.
    
    Based on the candidate's mentioned skills and technologies: {tech_stack}
    
    Generate 3-5 relevant technical questions that assess their proficiency.
    The questions should be:
    - Appropriate for their experience level
    - Specific to the technologies they mentioned
    - Not too easy, but not extremely difficult
    - Mix of conceptual and practical questions
    
    Format the response as a numbered list and be encouraging.
    """
```

**Design Rationale**:
- Context-aware question generation
- Balanced difficulty assessment
- Variety in question types
- Professional formatting requirements

### Temperature Settings Strategy
- **Information Extraction**: Temperature 0.3 (consistency and accuracy)
- **Question Generation**: Temperature 0.7 (creativity while maintaining relevance)
- **General Conversation**: Temperature 0.5 (balanced response variety)

##  Challenges & Solutions

### Challenge 1: Ollama Integration Complexity
**Problem**: Initial implementation struggled with Ollama's response object handling, particularly the `ollama._types.ListResponse` objects and model attribute access.

**Solution**: 
- Implemented robust response parsing with fallback mechanisms
- Added proper error handling for different response object types
- Created model detection logic with graceful degradation

```python
# Robust response handling
if hasattr(result, 'models'):
    models = result.models
    if hasattr(models[0], 'model'):
        self.model_name = models[0].model
```

### Challenge 2: Information Extraction Accuracy
**Problem**: Generic prompts led to inconsistent information extraction from user responses, particularly with varying input formats.

**Solution**:
- Designed structured prompts with clear field definitions
- Implemented hybrid approach combining regex patterns with LLM understanding
- Added validation layers for critical information (email, phone formats)

### Challenge 3: Conversation State Management
**Problem**: Determining when enough information was collected to proceed to technical questions proved challenging with varied user input patterns.

**Solution**:
- Implemented field-based completeness checking rather than message counting
- Added context accumulation across conversation turns
- Created state transition logic based on actual data presence

### Challenge 5: Error Handling and Resilience
**Problem**: Network interruptions and model loading failures caused application crashes.

**Solution**:
- Implemented comprehensive error handling with retry logic
- Added graceful degradation for service unavailability
- Created informative error messages for troubleshooting
