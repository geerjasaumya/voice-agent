# SuperBryn AI Voice Agent - Backend

A real-time AI voice agent built with LiveKit Agents framework for natural conversations and appointment management.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- API keys for: LiveKit, Deepgram, Cartesia, OpenAI

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Run

```bash
# Test configuration
python tests/test_config.py

# Start agent
python src/agent.py dev
```

## 📁 Project Structure

```
voice-agent-backend/
├── src/
│   ├── agent.py          # Main agent implementation
│   └── config.py         # Configuration management
├── tests/
│   └── test_config.py    # Configuration validator
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
└── README.md
```

## 🔧 Configuration

Required environment variables in `.env`:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
OPENAI_API_KEY=your_openai_key
```

## 🎯 Features (Phase 1)

- ✅ Real-time speech recognition (Deepgram)
- ✅ Natural language processing (OpenAI GPT-4o-mini)
- ✅ Text-to-speech synthesis (Cartesia)
- ✅ Low latency (<3 seconds)
- ✅ Conversation context maintenance
- ✅ Event logging and monitoring

## 📊 Performance

- **Latency**: 1-2.5 seconds average
- **Cost per minute**: ~$0.06-0.08
- **Free tiers**: Deepgram (200 hrs/month)

## 🔍 Testing

Connect to your agent:
1. Go to https://cloud.livekit.io
2. Navigate to your project's Playground
3. Connect and start speaking

## 🐛 Troubleshooting

**Agent not responding:**
- Verify all API keys in `.env`
- Check microphone permissions
- Review terminal logs

**High latency:**
- Check internet connection
- Verify LiveKit server region
- Consider using GPT-4o-mini instead of GPT-4

## 📝 Next Steps

- **Phase 2**: Tool calling & appointment booking
- **Phase 3**: Avatar integration
- **Phase 4**: Web frontend
- **Phase 5**: Deployment

## 📄 License

MIT