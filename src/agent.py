# """
# SuperBryn AI Voice Agent - Main Entry Point
# Phase 1: Basic Voice Loop (STT → LLM → TTS)
# Compatible with livekit-agents 1.3.12
# """

# import logging
# from datetime import datetime

# from livekit.agents import (
#     AutoSubscribe,
#     JobContext,
#     WorkerOptions,
#     cli,
#     llm,
# )
# from livekit.agents.voice import Agent as VoiceAgent
# from livekit.plugins import deepgram, cartesia, openai

# from config import config

# logger = logging.getLogger(__name__)


# class ConversationManager:
#     """Manages conversation state and context"""
    
#     def __init__(self):
#         self.conversation_id = None
#         self.start_time = None
#         self.user_phone = None
#         self.turn_count = 0
#         self.transcript_history = []
    
#     def start_conversation(self, room_name: str):
#         """Initialize a new conversation"""
#         self.conversation_id = f"{room_name}_{datetime.now().timestamp()}"
#         self.start_time = datetime.now()
#         logger.info(f"Started conversation: {self.conversation_id}")
    
#     def add_turn(self, speaker: str, text: str):
#         """Record a conversation turn"""
#         self.turn_count += 1
#         turn = {
#             "turn": self.turn_count,
#             "speaker": speaker,
#             "text": text,
#             "timestamp": datetime.now().isoformat()
#         }
#         self.transcript_history.append(turn)
    
#     def get_conversation_duration(self) -> float:
#         """Get conversation duration in seconds"""
#         if self.start_time:
#             return (datetime.now() - self.start_time).total_seconds()
#         return 0


# class AppointmentAgent:
#     """Main Voice Agent class handling the conversation pipeline"""
    
#     def __init__(self):
#         self.config = config
#         self.conversation_manager = ConversationManager()
        
#         # Initialize components
#         self.stt = self._init_stt()
#         self.tts = self._init_tts()
#         self.llm = self._init_llm()
        
#         self.system_prompt = self._create_system_prompt()
    
#     def _init_stt(self) -> deepgram.STT:
#         """Initialize Speech-to-Text"""
#         return deepgram.STT(
#             model=self.config.deepgram.model,
#             language=self.config.deepgram.language,
#         )
    
#     def _init_tts(self) -> cartesia.TTS:
#         """Initialize Text-to-Speech"""
#         return cartesia.TTS(
#             model=self.config.cartesia.model,
#             voice=self.config.cartesia.voice_id,
#         )
    
#     def _init_llm(self) -> openai.LLM:
#         """Initialize LLM"""
#         return openai.LLM(
#             model=self.config.llm.model,
#             temperature=self.config.llm.temperature,
#         )
    
#     def _create_system_prompt(self) -> str:
#         """Create the system prompt for the agent"""
#         return f"""You are {self.config.name}, a friendly and efficient AI voice assistant.

# IMPORTANT VOICE CONVERSATION RULES:
# 1. Keep responses SHORT - typically 1-2 sentences
# 2. Use natural speech (contractions, casual tone)
# 3. NO markdown, NO formatting, NO bullet points
# 4. Speak like you're talking to a friend
# 5. Ask ONE question at a time
# 6. Use conversational fillers when appropriate

# Your role:
# - Have natural conversations with users
# - Be warm, helpful, and professional
# - Listen carefully and respond appropriately
# - Keep the conversation flowing smoothly

# Example good responses:
# - "Hi! I'm here to help you with appointments. What can I do for you today?"
# - "Got it! I can help with that. Let me just get a few details from you."
# - "Perfect! I've got everything I need."

# Remember: You're having a VOICE conversation, not writing an email. Keep it natural and brief!"""
    
#     def create_voice_agent(self) -> VoiceAgent:
#         """Create the voice agent"""
#         logger.info("Creating voice agent")
        
#         # Create the voice agent with our components
#         agent = VoiceAgent(
#             stt=self.stt,
#             llm=self.llm,
#             tts=self.tts,
#             instructions=self.system_prompt,  
#         )
        
#         logger.info("Voice agent created successfully")
#         return agent
    
#     def setup_event_handlers(self, agent: VoiceAgent):
#         """Setup event handlers for the agent"""
        
#         @agent.on("user_speech_committed")
#         def on_user_speech(msg: llm.ChatMessage):
#             """Handler for when user speech is transcribed"""
#             text = msg.content if hasattr(msg, 'content') else str(msg)
#             logger.info(f"👤 User: {text}")
#             self.conversation_manager.add_turn("user", text)
            
#             duration = self.conversation_manager.get_conversation_duration()
#             logger.info(f"📊 Turn #{self.conversation_manager.turn_count} | Duration: {duration:.1f}s")
        
#         @agent.on("agent_speech_committed")
#         def on_agent_speech(msg: llm.ChatMessage):
#             """Handler for when agent speaks"""
#             text = msg.content if hasattr(msg, 'content') else str(msg)
#             logger.info(f"🤖 Agent: {text}")
#             self.conversation_manager.add_turn("agent", text)


# async def entrypoint(ctx: JobContext):
#     """Main entry point for the LiveKit agent"""
#     logger.info(f"🚀 Starting agent for room: {ctx.room.name}")
    
#     # Validate configuration
#     missing_keys = config.validate_required_keys()
#     if missing_keys:
#         logger.error(f"❌ Missing required API keys: {', '.join(missing_keys)}")
#         logger.error("Please check your .env file and ensure all required keys are set")
#         return
    
#     # Connect to room
#     await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
#     logger.info("✅ Connected to room")
    
#     # Create the appointment agent
#     appointment_agent = AppointmentAgent()
#     appointment_agent.conversation_manager.start_conversation(ctx.room.name)
    
#     # Create voice agent and setup handlers
#     agent = appointment_agent.create_voice_agent()
#     appointment_agent.setup_event_handlers(agent)
    
#     # Start the agent with the system prompt
#     agent.start(ctx.room, system_instruction=appointment_agent.system_prompt)
#     logger.info("✅ Agent started")
    
#     # Send initial greeting
#     await agent.say("Hi! I'm your appointment assistant. How can I help you today?")
#     logger.info("🎉 Agent ready for conversation!")


# if __name__ == "__main__":
#     """
#     Run the agent using LiveKit CLI
#     Usage: python src/agent.py dev
#     """
    
#     logging.basicConfig(
#         level=config.log_level,
#         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#     )
    
#     logger.info("=" * 50)
#     logger.info("🎙️ SuperBryn AI Voice Agent")
#     logger.info(f"Agent Name: {config.name}")
#     logger.info(f"LLM Model: {config.llm.model}")
#     logger.info(f"STT Model: {config.deepgram.model}")
#     logger.info(f"TTS Model: {config.cartesia.model}")
#     logger.info("=" * 50)
    
#     cli.run_app(
#         WorkerOptions(
#             entrypoint_fnc=entrypoint,
#         )
#     )
"""
SuperBryn AI Voice Agent - Phase 1 (Working)
Basic Voice Loop (STT → LLM → TTS)
Compatible with livekit-agents 1.3.12
"""

import logging

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice import AgentSession, Agent
from livekit.plugins import deepgram, cartesia, openai

from config import config

logger = logging.getLogger(__name__)


async def entrypoint(ctx: JobContext):
    """Main entry point for the LiveKit agent"""
    logger.info(f"🚀 Starting agent for room: {ctx.room.name}")
    
    # Validate configuration
    missing_keys = config.validate_required_keys()
    if missing_keys:
        logger.error(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        logger.error("Please check your .env file and ensure all required keys are set")
        return
    
    # Connect to room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("✅ Connected to room")
    
    # System prompt for the agent
    system_prompt = f"""You are {config.name}, a friendly and efficient AI voice assistant.

IMPORTANT VOICE CONVERSATION RULES:
1. Keep responses SHORT - typically 1-2 sentences
2. Use natural speech (contractions, casual tone)
3. NO markdown, NO formatting, NO bullet points
4. Speak like you're talking to a friend
5. Ask ONE question at a time
6. Use conversational fillers when appropriate

Your role:
- Have natural conversations with users
- Be warm, helpful, and professional
- Listen carefully and respond appropriately
- Keep the conversation flowing smoothly

Example good responses:
- "Hi! I'm here to help you with appointments. What can I do for you today?"
- "Got it! I can help with that. Let me just get a few details from you."
- "Perfect! I've got everything I need."

Remember: You're having a VOICE conversation, not writing an email. Keep it natural and brief!"""
    
    # Create an Agent with the instructions
    agent = Agent(
        stt=deepgram.STT(
            model=config.deepgram.model,
            language=config.deepgram.language,
        ),
        llm=openai.LLM(
            model=config.llm.model,
            temperature=config.llm.temperature,
        ),
        tts=cartesia.TTS(
            model=config.cartesia.model,
            voice=config.cartesia.voice_id,
        ),
        instructions=system_prompt,
    )
    
    logger.info("✅ Agent created")
    
    # Create the agent session
    session = AgentSession()
    
    logger.info("✅ Agent session created")
    
    # Start the session with the agent AND the room
    await session.start(agent, room=ctx.room)
    
    logger.info("✅ Agent session started")
    
    # Send initial greeting
    await session.say("Hi! I'm your appointment assistant. How can I help you today?")
    
    logger.info("🎉 Agent ready for conversation!")


if __name__ == "__main__":
    """
    Run the agent using LiveKit CLI
    Usage: python src/agent.py dev
    """
    
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger.info("=" * 50)
    logger.info("🎙️ SuperBryn AI Voice Agent")
    logger.info(f"Agent Name: {config.name}")
    logger.info(f"LLM Model: {config.llm.model}")
    logger.info(f"STT Model: {config.deepgram.model}")
    logger.info(f"TTS Model: {config.cartesia.model}")
    logger.info("=" * 50)
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )