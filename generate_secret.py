import secrets
import string

def generate_secret_key(length=64):
    """Genera una clave secreta segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("🔐 Generando clave secreta para producción...")
    secret_key = generate_secret_key()
    print(f"\n✅ Clave generada:")
    print(f"SECRET_KEY={secret_key}")
    print("\n📝 Copia esta clave y úsala en tus variables de entorno de producción")
    print("⚠️  IMPORTANTE: No compartas esta clave públicamente")
