"""
Real Telegram Bot API Client Dispatcher.
Implements sendMessage, sendPhoto (with native multipart/form-data upload for raster PNG/JPG & fallback for SVG documents), sendDocument, sendMediaGroup, editMessageText, editMessageReplyMarkup, and answerCallbackQuery.
Uses TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.
"""

import os
import json
import uuid
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
        
        # Strip out any keys with None values before JSON encoding
        clean_payload = {k: v for k, v in payload.items() if v is not None}
        data = json.dumps(clean_payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                res_bytes = resp.read()
                res_text = res_bytes.decode("utf-8")
                return json.loads(res_text)
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
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
        if not self.is_configured:
            return {"ok": False, "description": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in environment (.env)"}

        # If it's a local file path on disk, upload via multipart/form-data
        if os.path.isfile(photo_url_or_path):
            return self.send_photo_file(photo_url_or_path, caption=caption, reply_markup=reply_markup)

        payload: Dict[str, Any] = {
            "chat_id": self.chat_id,
            "photo": photo_url_or_path
        }
        if caption:
            payload["caption"] = caption
        if reply_markup:
            payload["reply_markup"] = reply_markup
        return self._post("sendPhoto", payload)

    def send_photo_file(self, file_path: str, caption: Optional[str] = None, reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not self.is_configured:
            return {"ok": False, "description": "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in environment (.env)"}

        if not os.path.isfile(file_path):
            return {"ok": False, "description": f"Image file '{file_path}' not found on disk"}

        # Telegram sendPhoto only accepts PNG/JPG raster files. SVG files must use sendDocument.
        is_svg = file_path.lower().endswith(".svg")
        api_method = "sendDocument" if is_svg else "sendPhoto"
        file_field_name = "document" if is_svg else "photo"

        boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
        url = f"{self.api_url}/{api_method}"
        masked_url = f"https://api.telegram.org/bot***masked***/{api_method}"

        body = bytearray()
        
        # chat_id field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{self.chat_id}\r\n'.encode("utf-8"))
        
        # caption field
        if caption:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode("utf-8"))

        # reply_markup field
        if reply_markup:
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="reply_markup"\r\n\r\n{json.dumps(reply_markup)}\r\n'.encode("utf-8"))

        # photo/document file field
        filename = os.path.basename(file_path)
        mime_type = "image/svg+xml" if is_svg else "image/png" if filename.endswith(".png") else "image/jpeg"
        
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{file_field_name}"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        
        with open(file_path, "rb") as f:
            body.extend(f.read())
        body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

        req = urllib.request.Request(url, data=bytes(body), headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        })

        print(f"[Telegram Debug] Uploading image file '{filename}' via {api_method} to {masked_url}")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_bytes = resp.read()
                res_text = res_bytes.decode("utf-8")
                return json.loads(res_text)
        except urllib.error.HTTPError as e:
            try:
                err_body = e.read().decode("utf-8")
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
            return {"ok": False, "description": str(e)}

    def send_media_group(self, media_urls: List[str], caption: Optional[str] = None) -> Dict[str, Any]:
        media = []
        for i, url in enumerate(media_urls):
            item = {"type": "photo", "media": url}
            if i == 0 and caption:
                item["caption"] = caption
            media.append(item)

        payload = {
            "chat_id": self.chat_id,
            "media": media
        }
        return self._post("sendMediaGroup", payload)

    def edit_message_text(self, message_id: int, text: str, reply_markup: Optional[Dict[str, Any]] = None, parse_mode: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "chat_id": self.chat_id,
            "message_id": message_id,
            "text": text
        }
        if parse_mode:
            payload["parse_mode"] = parse_mode
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
