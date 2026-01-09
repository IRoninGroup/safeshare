Remove GPS, device info, timestamps, and other identifying metadata from photos and videos.

## Features

- ✅ Removes ALL metadata from images (EXIF, GPS, device info, timestamps)
- ✅ Removes ALL metadata from videos (using ffmpeg re-encoding)
- ✅ Multiple interfaces: Telegram bot, CLI, easy to extend
- ✅ Secure file handling with automatic cleanup
- ✅ Modular architecture for easy extension

## Installation

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Install ffmpeg (for video processing)

**Arch:**
```bash
sudo pacman -S ffmpeg
#or
yay -S ffmpeg-git
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### 3. Configure

**Option A: Environment variable (recommended)**
```bash
export TELEGRAM_BOT_TOKEN="your_token_from_botfather"
```

**Option B: Copy and edit .env file**
```bash
cp .env.example .env
# Edit .env and add your token
```

## Usage

### Telegram Bot

1. **Create your bot:**
   - Talk to [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the token

2. **Run the bot:**
```bash
python main.py
```

3. **Use the bot:**
   - Search for your bot in Telegram
   - Send `/start`
   - Send photos or videos
   - Receive cleaned files

### Command Line Interface

Process a single file:
```bash
python -m clients.cli input.jpg output.jpg
```

With options:
```bash
python -m clients.cli input.mp4 output.mp4 --type video --verbose
```

## Project Structure

```
safesend/
├── core/                      # Core business logic
│   ├── metadata_remover.py   # Metadata removal algorithms
│   ├── file_handler.py       # Secure file operations
│   └── validators.py         # File validation
├── clients/                   # Client interfaces
│   ├── telegram_bot.py       # Telegram bot
│   └── cli.py                # Command-line interface
├── config.py                  # Configuration
├── main.py                    # Entry point
└── requirements.txt
```

## Security Notes

⚠️ **This tool removes metadata, but:**
- Visual content can still identify locations/people
- Use additional security measures (VPN, Tor)
- Turn off location services before taking photos
- Verify metadata removal with viewer tools
- Consider operational security best practices

## Extending

Add new clients easily by importing core modules:

```python
from core import MetadataRemover, SecureFileHandler

remover = MetadataRemover()
handler = SecureFileHandler()

# Use in your Discord bot, web API, etc.
success, error = remover.remove_image_metadata(input, output)
```

## Testing

Run tests:
```bash
python -m pytest tests/
```

Or with unittest:
```bash
python -m unittest tests/test_metadata_remover.py
```

## License

Use responsibly and ethically to protect privacy.

## Support

For issues or questions, please open an issue on the repository.