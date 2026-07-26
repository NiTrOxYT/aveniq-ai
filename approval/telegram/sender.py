"""
Real Telegram Bot API Client Dispatcher.
Implements sendMessage, sendPhoto, sendMediaGroup, editMessageText, editMessageReplyMarkup, and answerCallbackQuery.
Uses TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

class TelegramSender:
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None

    @property
    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def _post(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_configured:
            return {"ok": False, "description": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in environment (Mock fallback mode)"}

        url = f"{self.api_url}/{method}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_bytes = resp.read()
                return json.loads(res_bytes.decode("utf-8"))
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_message(self, text: str, reply_markup: Optional[Dict[str, Any]] = None, parse_mode: str = "Markdown") -> Dict[str, Any]:
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("sendMessage", payload)

    def send_photo(self, photo_url_or_path: str, caption: Optional[str] = None, reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "chat_id": self.chat_id,
            "photo": photo_url_or_path
        }
        if caption:
            payload["caption"] = caption
            payload["parse_mode"] = "Markdown"
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("sendPhoto", payload)

    def send_media_group(self, media_urls: List[str], caption: Optional[str] = None) -> Dict[str, Any]:
        media = []
        for i, url in enumerate(media_urls):
            item = {"type": "photo", "media": url}
            if i == 0 and caption:
                item["caption"] = caption
                item["parse_mode"] = "Markdown"
            media.append(item)
        payload = {
            "chat_id": self.chat_id,
            "media": media
        }
        return self._post("sendMediaGroup", payload)

    def edit_message_text(self, message_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("editMessageText", payload)

    def edit_message_reply_markup(self, message_id: int, reply_markup: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "reply_markup": reply_markup
        }
        return self._post("editMessageReplyMarkup", payload)

    def answer_callback_query(self, callback_query_id: str, text: Optional[str] = None, show_alert: bool = False) -> Dict[str, Any]:
        payload = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert
        }
        if text:
            payload["text"] = text
        return self._post("answerCallbackQuery", payload)

global_telegram_sender = TelegramSender()
