"""Tests for account endpoints and security policy."""

import unittest

from service import create_app


class AccountsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "CORS_ORIGINS": "http://localhost:3000",
        })
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_create_read_update_delete_account(self):
        created = self.client.post(
            "/api/accounts",
            json={"name": "Asha Patil", "email": "asha@example.com"},
        )
        self.assertEqual(created.status_code, 201)
        account_id = created.get_json()["id"]

        read = self.client.get(f"/api/accounts/{account_id}")
        self.assertEqual(read.status_code, 200)
        self.assertEqual(read.get_json()["name"], "Asha Patil")

        updated = self.client.put(
            f"/api/accounts/{account_id}",
            json={"name": "Asha P.", "email": "asha.p@example.com"},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["name"], "Asha P.")

        deleted = self.client.delete(f"/api/accounts/{account_id}")
        self.assertEqual(deleted.status_code, 200)
        self.assertTrue(deleted.get_json()["deleted"])
        self.assertEqual(
            self.client.get(f"/api/accounts/{account_id}").status_code, 404
        )

    def test_list_accounts(self):
        self.client.post(
            "/api/accounts",
            json={"name": "Ravi", "email": "ravi@example.com"},
        )
        response = self.client.get("/api/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.get_json()["count"], 1)

    def test_validation(self):
        self.assertEqual(self.client.post("/api/accounts", json={}).status_code, 400)
        self.assertEqual(
            self.client.post("/api/accounts", data="not-json").status_code, 400
        )

    def test_security_headers(self):
        response = self.client.get("/api/health")
        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")

    def test_cors_policy(self):
        response = self.client.get(
            "/api/health", headers={"Origin": "http://localhost:3000"}
        )
        self.assertEqual(
            response.headers.get("Access-Control-Allow-Origin"),
            "http://localhost:3000",
        )


if __name__ == "__main__":
    unittest.main()
