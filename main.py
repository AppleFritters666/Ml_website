from Website import create_app
import mysql.connector

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

