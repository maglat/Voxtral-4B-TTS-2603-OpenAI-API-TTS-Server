# Voxtral-4B-TTS-2603 Docker Setup

OpenAI-kompatibler TTS-Server für das Voxtral-4B-TTS-2603 Modell von Mistral.

## Schnellstart

### 1. HuggingFace Token einrichten

```bash
# Token von https://huggingface.co/settings/tokens holen
cp .env.example .env
# Bearbeite .env und füge deinen HF_TOKEN ein
```

### 2. Docker Container starten

```bash
docker-compose up --build
```

Der Server startet auf `http://localhost:4576`

## OpenAI-kompatible API

### Sprachgenerierung (Text-to-Speech)

```bash
curl -X POST http://localhost:4576/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hallo, das ist ein Test.",
    "model": "mistralai/Voxtral-4B-TTS-2603",
    "voice": "de_female",
    "response_format": "wav"
  }' -o output.wav
```

### Verfügbare Voices (für Deutsch)

- `de_female` - Deutsche weibliche Stimme
- `de_male` - Deutsche männliche Stimme

### Andere verfügbare Voices

- `en_female`, `en_male` - Englisch
- `fr_female`, `fr_male` - Französisch
- `es_female`, `es_male` - Spanisch
- `it_female`, `it_male` - Italienisch
- `pt_female`, `pt_male` - Portugiesisch
- `nl_female`, `nl_male` - Niederländisch
- `ar_male` - Arabisch
- `hi_female`, `hi_male` - Hindi

### Audio-Formate

- `wav` (Standard)
- `mp3`
- `flac`
- `opus`
- `pcm`

## Open WebUI Integration

In Open WebUI kannst du den TTS-Service wie folgt nutzen:

```
API URL: http://<server-ip>:4576
Model: "mistralai/Voxtral-4B-TTS-2603"
Voice: "de_female"
```

Die OpenAI-kompatible API ist unter `/v1/audio/speech` erreichbar.

## API Reference

### GET /v1/audio/voices

Listet alle verfügbaren Voices:

```bash
curl http://localhost:4576/v1/audio/voices
```

### POST /v1/audio/speech

Generiert Sprachaudio aus Text.

**Request Body:**
```json
{
  "input": "Der zu sprechende Text",
  "model": "mistralai/Voxtral-4B-TTS-2603",
  "voice": "de_female",
  "response_format": "wav"
}
```

## Modell-Info

- **Modell:** Voxtral-4B-TTS-2603 von Mistral
- **Sprachen:** 9 Sprachen inkl. Deutsch
- **Voices:** 20 vordefinierte Stimmen
- **Audio Sample Rate:** 24 kHz
- **GPU-Anforderung:** Min. 16GB VRAM
- **Lizenz:** CC-BY-NC-4.0 (nicht-kommerziell)

## Hardware-Anforderungen

- NVIDIA GPU (min. 16GB VRAM empfohlen)
- CUDA 12.9+
- Min. 32GB RAM

CC-BY-NC-4.0 - Nicht-kommerzielle Nutzung
