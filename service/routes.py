"""REST endpoints for customer accounts."""

from uuid import uuid4

from flask import Blueprint, jsonify, request

api = Blueprint("accounts_api", __name__)
_ACCOUNTS = {}


def _error(message, status):
    return jsonify({"error": message}), status


@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "accounts"}), 200


@api.post("/accounts")
def create_account():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error("Request body must be a JSON object", 400)
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip()
    if not name or not email:
        return _error("Both name and email are required", 400)
    account_id = str(uuid4())
    account = {"id": account_id, "name": name, "email": email}
    _ACCOUNTS[account_id] = account
    return jsonify(account), 201


@api.get("/accounts")
def list_accounts():
    return jsonify({"accounts": list(_ACCOUNTS.values()),
                    "count": len(_ACCOUNTS)}), 200


@api.get("/accounts/<account_id>")
def read_account(account_id):
    account = _ACCOUNTS.get(account_id)
    if account is None:
        return _error("Account not found", 404)
    return jsonify(account), 200


@api.put("/accounts/<account_id>")
def update_account(account_id):
    account = _ACCOUNTS.get(account_id)
    if account is None:
        return _error("Account not found", 404)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error("Request body must be a JSON object", 400)
    name = str(payload.get("name", account["name"])).strip()
    email = str(payload.get("email", account["email"])).strip()
    if not name or not email:
        return _error("Both name and email must be non-empty", 400)
    account.update({"name": name, "email": email})
    return jsonify(account), 200


@api.delete("/accounts/<account_id>")
def delete_account(account_id):
    account = _ACCOUNTS.pop(account_id, None)
    if account is None:
        return _error("Account not found", 404)
    return jsonify({"deleted": True, "id": account_id}), 200
