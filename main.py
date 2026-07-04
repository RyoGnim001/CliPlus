from apiflask import APIFlask
from app.routes.me import bp as me_bp

app = APIFlask(__name__)
app.register_blueprint(me_bp)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)