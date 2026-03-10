from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Escáner PRO</title>

<script src="https://unpkg.com/@zxing/library@latest"></script>

<style>
    body {
        font-family: Arial;
        text-align: center;
        background: #0f0f0f;
        color: white;
    }
    video {
        width: 90%;
        max-width: 400px;
        border-radius: 15px;
        margin-top: 20px;
        border: 2px solid #00ff88;
    }
    .result {
        margin-top: 20px;
        font-size: 18px;
        color: #00ff88;
        word-wrap: break-word;
        padding: 10px;
    }
</style>
</head>

<body>

<h2>📷 Escáner QR + Código de Barras PRO</h2>

<video id="video" autoplay playsinline></video>
<div class="result" id="resultado">Iniciando cámara...</div>

<script>
const codeReader = new ZXing.BrowserMultiFormatReader();
const video = document.getElementById("video");
const resultado = document.getElementById("resultado");

let lastResult = "";

// 🔥 Iniciar cámara BIEN (modo PRO)
async function iniciar() {
    try {
        await codeReader.decodeFromConstraints(
            {
                video: {
                    facingMode: { ideal: "environment" } // 🔥 cámara trasera
                }
            },
            video,
            (result, err) => {

                if (result) {
                    if (result.text !== lastResult) {
                        lastResult = result.text;

                        resultado.innerHTML = "Resultado:<br>" + result.text;

                        // 🔊 sonido
                        new Audio("https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg").play();

                        // 🔥 abrir links automáticamente
                        if (result.text.startsWith("http")) {
                            setTimeout(() => {
                                window.open(result.text, "_blank");
                            }, 800);
                        }
                    }
                }

                // Evita spam de errores
                if (err && !(err instanceof ZXing.NotFoundException)) {
                    console.error(err);
                }
            }
        );
    } catch (error) {
        resultado.innerText = "❌ No se pudo acceder a la cámara";
        console.error(error);
    }
}

iniciar();
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    