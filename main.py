from apiflask import APIFlask
from app.routes.me import bp as me_bp
from app.routes.pacientes import bp as pacientes_bp
from app.routes.consultas import bp as consultas_bp
from app.routes.comprovante import bp as comprovante_bp

app = APIFlask(__name__)

#Autenticão no Swagger
app.security_schemes = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}



app.register_blueprint(me_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(consultas_bp)
app.register_blueprint(comprovante_bp)

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)