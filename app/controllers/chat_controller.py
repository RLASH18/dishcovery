from flask import request, jsonify
from flask_login import current_user
from app.services.chat_service import ChatService

class ChatController:

    @staticmethod
    def new_chat():
        if not current_user.is_authenticated:
            return jsonify({ "error": "Unauthorized" }), 401

        chat = ChatService.create_chat(current_user.id)

        return jsonify({ "chat_id": chat.id }), 201
    
    @staticmethod
    def get_chats():
        if not current_user.is_authenticated:
            return jsonify([]), 200

        chats = ChatService.get_user_chats(current_user.id)

        return jsonify([
            {
                "id": c.id,
                "title": c.title,
                "updated_at": c.updated_at.isoformat()
            }
            for c in chats
        ])
    
    @staticmethod
    def get_messages(chat_id):
        messages = ChatService.get_messages(chat_id)

        return jsonify([
            {"role": m.role, "content": m.content}
            for m in messages
        ])
    
    @staticmethod
    def send_message(chat_id):
        data = request.get_json()
        user_input = data.get('message', '').strip()

        if not user_input:
            return jsonify({ "error": "Message cannot be empty" }), 400
        
        ai_reply, title = ChatService.send_message(chat_id, user_input)

        return jsonify({ "reply": ai_reply, "title": title })
    
    @staticmethod
    def delete_chat(chat_id):
        ChatService.delete_chat(chat_id)

        return jsonify({ "message": "Chat deleted" })
