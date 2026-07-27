"""
Real Telegram Bot API Client Dispatcher.
Implements sendMessage, sendPhoto, sendMediaGroup, editMessageText, editMessageReplyMarkup, and answerCallbackQuery.
Uses TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, List, Optional

class TelegramSender:
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = (bot_token or os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
        self.chat_id = (chat_id or os.environ.get("TELEGRAM_CHAT_ID") or "").strip()
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None

    @property
    def is_configured(self) -> bool:
        return bool(self.bot_token and self.chat_id)

    def _post(self, method: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_configured:
            return {"ok": False, "description": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in environment (.env)"}

        url = f"{self.api_url}/{method}"
        masked_url = f"https://api.telegram.org/bot***masked***/{method}"
        
        # Strip out any keys with None values before JSON encoding to avoid Telegram API 400 Bad Request
        clean_payload = {k: v for k, v in payload.items() if v is not None}
        data = json.dumps(clean_payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        print(f"[Telegram Debug] Dispatching request to {masked_url}")
        print(f"[Telegram Debug] Target chat_id: {self.chat_id}")
        print(f"[Telegram Debug] Payload: {json.dumps(clean_payload)}")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_bytes = resp.read()
                res_text = res_bytes.decode("utf-8")
                print(f"[Telegram Debug] Response Code: {resp.status}")
                print(f"[Telegram Debug] Response Body: {res_text}")
                return json.loads(res_text)
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
                print(f"[Telegram Debug] HTTP Error Code: {e.code}")
                print(f"[Telegram Debug] Error Body: {err_body}")
                err_json = json.loads(err_body)
                return {
                    "ok": False,
                    "error_code": err_json.get("error_code", e.code),
                    "description": err_json.get("description", e.reason),
                    "raw_response": err_json
                }
            except Exception:
                return {
                    "ok": False,
                    "error_code": e.code,
                    "description": f"HTTP Error {e.code}: {e.reason}"
                }
        except Exception as e:
            print(f"[Telegram Debug] Exception: {str(e)}")
            return {"ok": False, "description": str(e)}

    def send_message(self, text: str, reply_markup: Optional[Dict[str, Any]] = None, parse_mode: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": self.chat_id,
            "text": text
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("sendMessage", payload)

    def send_photo(self, photo_url_or_path: str, caption: Optional[str] = None, reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
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

    def edit_message_text(self, message_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None, parse_mode: str = "Markdown") -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("editMessageText", payload)

    def edit_message_reply_markup(self, message_id: int, reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": self.chat_id,
            "message_id": message_id
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("editMessageReplyMarkup", payload)

    def answer_callback_query(self, callback_query_id: str, text: Optional[str] = None, show_alert: bool = False) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "callback_query_id": callback_query_id,
            "show_alert": show_alert
        }
        if text:
            payload["text"] = text
        return self._post("answerCallbackQuery", payload)
