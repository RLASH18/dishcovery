import os
import google.generativeai as genai
from flask import current_app
from app import db
from app.models.chat import Chat
from app.models.message import Message
from app.services.mealdb_service import MealDbService

class ChatService:
    
    @staticmethod
    def _load_system_prompt():
        """Load the AI system prompt from the markdown file"""
        prompt_path = os.path.join(
            os.path.dirname(__file__), '../prompts/system_prompt.md'
        )
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def _get_model():
        """Initialize and return the Gemini GenerativeModel with Tools"""
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])

        # Register tools (Function Calling)
        tools = [
            MealDbService.search_by_ingredient,
            MealDbService.get_recipe_details,
            MealDbService.search_by_name
        ]

        return genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            system_instruction=ChatService._load_system_prompt(),
            tools=tools
        )
    
    @staticmethod
    def create_chat(user_id):
        """Create and persist a new chat session"""
        chat = Chat(user_id=user_id, title="New Chat")

        db.session.add(chat)
        db.session.commit()

        return chat
    
    @staticmethod
    def get_user_chats(user_id):
        """Fetch all chat sessions for a user, ordered by latest"""
        return Chat.query.filter_by(user_id=user_id) \
                         .order_by(Chat.updated_at.desc()) \
                         .all()
    
    @staticmethod
    def delete_chat(chat_id):
        """Delete a chat session and cascade-delete its messages"""
        chat = db.get_or_404(Chat, chat_id)

        db.session.delete(chat)
        db.session.commit()

    
    @staticmethod
    def get_messages(chat_id):
        """Fetch all messages for a given chat session"""
        return Message.query.filter_by(chat_id=chat_id) \
                            .order_by(Message.created_at) \
                            .all()
    
    @staticmethod
    def send_message(chat_id, user_input):
        """
        Handles a user message, sends it to Gemini with chat context,
        and saves both the user input and AI response.
        """
        chat = db.get_or_404(Chat, chat_id)

        # Load past messages for context
        past_messages = Message.query.filter_by(chat_id=chat_id) \
                                     .order_by(Message.created_at).all()
        
        # Build Gemini-compatible history
        history = [
            {"role": msg.role, "parts": [msg.content]}
            for msg in past_messages
        ]

        # Auto-title on first message
        if chat.title == "New Chat" and not past_messages:
            chat.title = user_input[:40] + ("..." if len(user_input) > 40 else "")
        
        # Save user message
        user_msg = Message(chat_id=chat_id, role="user", content=user_input)

        db.session.add(user_msg)

        # Call Gemini with automatic tool execution (enable_automatic_function_calling=True)
        model = ChatService._get_model()
        chat_session = model.start_chat(history=history, enable_automatic_function_calling=True)
        response = chat_session.send_message(user_input)
        ai_reply = response.text

        # Save AI reply
        ai_msg = Message(chat_id=chat_id, role="model", content=ai_reply)

        db.session.add(ai_msg)

        db.session.commit()

        return ai_reply, chat.title
