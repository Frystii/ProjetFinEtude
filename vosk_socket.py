from vosk import Model, KaldiRecognizer
import pyaudio
import json
import socket

# Configuration du modèle Vosk et des sockets
MODEL_PATH = "vosk_model/vosk-model-small-en-us-0.15"  # Remplacez par le chemin de votre modèle
SERVER_IP = "10.77.3.117"  # Remplacez par l'adresse IP de la VM
SERVER_PORT = 5000  # Port d'écoute sur la VM

def main():
    # Charger le modèle Vosk
    print("Chargement du modèle...")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    # Configurer l'entrée audio avec PyAudio
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    # Configurer le client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connecté au serveur {SERVER_IP}:{SERVER_PORT}")

        print("Modèle chargé. Parlez dans le micro.")
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                # Décodage du résultat
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    # Vérification des mots-clés
                    if "save" in text or "go to" in text:
                        print(f"Phrase reconnue : {text}")
                        # Envoyer la phrase reconnue au serveur
                        client_socket.sendall(text.encode("utf-8"))
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()

if __name__ == "__main__":
    main()
