"""Run the Customer Accounts service on port 8080."""

import os

from service import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8080")), debug=False)
