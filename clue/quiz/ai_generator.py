# quiz/ai_generator.py - Simplified version
import os
import json
import requests
from django.conf import settings
from django.core.cache import cache
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AIQuestionGenerator:
    """Generate quiz questions using OpenRouter AI API with single key"""
    
    def __init__(self, model='grok'):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = model
        self.api_url = settings.OPENROUTER_API_URL
        
        # Get the actual OpenRouter model name
        self.openrouter_model = settings.OPENROUTER_MODEL_MAP.get(
            model, 
            settings.OPENROUTER_MODEL_MAP['grok']  # Default to Grok
        )
        
    def generate_questions(self, topic: str, difficulty: str = 'medium', num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions using OpenRouter"""
        
        # Validate input
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        
        num_questions = min(num_questions, settings.MAX_AI_QUESTIONS)
        
        # Check cache first
        cache_key = f"ai_questions_{topic}_{difficulty}_{num_questions}_{self.model}"
        cached = cache.get(cache_key)
        if cached:
            logger.info(f"Using cached questions for {cache_key}")
            return cached
        
        # Build the prompt
        prompt = self._build_prompt(topic, difficulty, num_questions)
        
        try:
            questions = self._call_openrouter_api(prompt)
            
            # Cache successful results for 30 minutes
            cache.set(cache_key, questions, 1800)
            logger.info(f"Generated {len(questions)} questions using {self.model}")
            
            return questions
            
        except Exception as e:
            logger.error(f"AI generation failed: {str(e)}")
            # Return fallback questions instead of raising exception
            return self._get_fallback_questions(topic, difficulty, num_questions)
    
    def _build_prompt(self, topic: str, difficulty: str, num_questions: int) -> str:
        """Build the prompt for AI generation"""
        
        difficulty_map = {
            'easy': 'beginner level',
            'medium': 'intermediate level',
            'hard': 'advanced level'
        }
        
        difficulty_text = difficulty_map.get(difficulty, 'intermediate level')
        
        return f"""You are an expert quiz question generator for an educational platform.

Generate exactly {num_questions} multiple-choice questions about "{topic}" at {difficulty_text}.

CRITICAL FORMATTING REQUIREMENTS - FOLLOW EXACTLY:
For EACH question, use this EXACT format:

Question: [The question text]
Options:
A) [Option A text]
B) [Option B text]
C) [Option C text]
D) [Option D text]
Correct: [Single letter A, B, C, or D]
Explanation: [Brief explanation why the correct answer is right]

IMPORTANT:
- Only ONE correct answer per question
- Make incorrect options plausible but clearly wrong
- Questions should test understanding, not just memorization
- Vary question types (definition, application, analysis, etc.)
- Keep explanations concise but informative

Do not include any additional text before, between, or after the questions."""
    
    def _call_openrouter_api(self, prompt: str) -> List[Dict]:
        """Call OpenRouter API with single API key"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://learningmanagementsystem.com",
            "X-Title": "Learning Management System"
        }
        
        payload = {
            "model": self.openrouter_model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful educational assistant that generates quiz questions in a strict format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 3000,
            "top_p": 0.9,
        }
        
        try:
            response = requests.post(
                self.api_url, 
                json=payload, 
                headers=headers, 
                timeout=45  # Increased timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return self._parse_response(content)
            elif response.status_code == 401:
                logger.error("Invalid OpenRouter API key")
                raise Exception("Invalid API configuration. Please contact administrator.")
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded")
                raise Exception("Rate limit exceeded. Please try again in a moment.")
            else:
                logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                raise Exception(f"AI service error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error("OpenRouter API timeout")
            raise Exception("AI service is taking too long. Please try again.")
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter network error: {str(e)}")
            raise Exception("Network error. Please check your connection.")
    
    def _parse_response(self, text: str) -> List[Dict]:
        """Parse AI response into structured questions"""
        questions = []
        lines = text.strip().split('\n')
        
        current_question = None
        collecting_options = False
        option_patterns = ['A)', 'B)', 'C)', 'D)']
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Detect new question
            if line.startswith('Question:'):
                if current_question:
                    if self._validate_question(current_question):
                        questions.append(current_question)
                
                current_question = {
                    'content': line[9:].strip(),  # Remove "Question:"
                    'choices': [],
                    'correct': '',
                    'explanation': '',
                    'is_valid': True
                }
                collecting_options = False
            
            # Start options section
            elif line.startswith('Options:'):
                collecting_options = True
            
            # Parse options (A), B), C), D))
            elif collecting_options and current_question:
                for pattern in option_patterns:
                    if line.startswith(pattern):
                        option_text = line[len(pattern):].strip()
                        current_question['choices'].append({
                            'letter': pattern[0],  # 'A', 'B', 'C', or 'D'
                            'text': option_text
                        })
                        break
            
            # Parse correct answer
            elif line.startswith('Correct:'):
                if current_question:
                    correct_letter = line[8:].strip().upper()
                    if correct_letter in ['A', 'B', 'C', 'D']:
                        current_question['correct'] = correct_letter
            
            # Parse explanation
            elif line.startswith('Explanation:'):
                if current_question:
                    current_question['explanation'] = line[12:].strip()
            
            # Continue explanation if multi-line
            elif current_question and current_question['explanation'] and not any([
                line.startswith('Question:'),
                line.startswith('Options:'),
                line.startswith('Correct:'),
                line.startswith('Explanation:')
            ]):
                current_question['explanation'] += ' ' + line
        
        # Add the last question
        if current_question and self._validate_question(current_question):
            questions.append(current_question)
        
        # Ensure we have valid questions
        valid_questions = [q for q in questions if self._validate_question(q)]
        
        if not valid_questions:
            raise Exception("No valid questions could be parsed from the AI response")
        
        return valid_questions
    
    def _validate_question(self, question: Dict) -> bool:
        """Validate that a question has all required fields"""
        # Check required fields
        if not question.get('content'):
            return False
        
        if len(question.get('choices', [])) != 4:
            return False
        
        if not question.get('correct'):
            return False
        
        # Validate correct answer is A, B, C, or D
        correct = question['correct'].upper()
        if correct not in ['A', 'B', 'C', 'D']:
            return False
        
        # Validate all choices have letters A-D
        choice_letters = [c['letter'].upper() for c in question['choices']]
        if sorted(choice_letters) != ['A', 'B', 'C', 'D']:
            return False
        
        # Validate correct choice exists
        correct_choice_exists = any(
            c['letter'].upper() == correct 
            for c in question['choices']
        )
        
        return correct_choice_exists
    
    def _get_fallback_questions(self, topic: str, difficulty: str, num_questions: int) -> List[Dict]:
        """Return fallback questions if AI fails"""
        logger.warning(f"Using fallback questions for topic: {topic}")
        
        fallbacks = [
            {
                'content': f'What is the primary purpose of studying {topic}?',
                'choices': [
                    {'letter': 'A', 'text': 'To understand fundamental concepts'},
                    {'letter': 'B', 'text': 'To memorize facts'},
                    {'letter': 'C', 'text': 'To pass exams only'},
                    {'letter': 'D', 'text': 'To complicate simple ideas'}
                ],
                'correct': 'A',
                'explanation': f'Studying {topic} helps understand fundamental concepts that can be applied in various contexts.'
            },
            {
                'content': f'Which approach is most effective for mastering {topic}?',
                'choices': [
                    {'letter': 'A', 'text': 'Practice and application'},
                    {'letter': 'B', 'text': 'Theoretical study only'},
                    {'letter': 'C', 'text': 'Avoiding mistakes'},
                    {'letter': 'D', 'text': 'Rote memorization'}
                ],
                'correct': 'A',
                'explanation': f'Practice and real-world application are key to mastering {topic}.'
            }
        ]
        
        # Return requested number of questions (repeating if necessary)
        return fallbacks[:min(num_questions, len(fallbacks))]
