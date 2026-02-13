"""
Chord DHT Themed Chatbot GUI
An attractive, professional terminal UI for the Chord DHT knowledge base chatbot
"""

from huggingface_hub import InferenceClient
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.align import Align
from rich.live import Live
from rich.spinner import Spinner
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Initialize Hugging Face client
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(model="openai/gpt-oss-20b", token=HF_TOKEN)

# Color scheme for Chord DHT theme
CHORD_THEME = {
    "primary": "#FF6B9D",      # Pink/Magenta for Chord ring
    "secondary": "#00D9FF",    # Cyan for nodes
    "success": "#00FF9F",      # Green for positive
    "warning": "#FFD93D",      # Yellow for warnings
    "bg_dark": "#0A0E27",      # Dark blue background
    "text_light": "#E8E8E8"    # Light text
}

class ChordChatbotGUI:
    def __init__(self):
        self.console = Console()
        self.conversation_history = []
        self.session_start = datetime.now()
        self.display_banner()
        
    def display_banner(self):
        """Display the Chord DHT themed banner"""
        banner_text = """
        ╔═══════════════════════════════════════════════════════╗
        ║                                                       ║
        ║    ⟡ CHORD DHT KNOWLEDGE BASE CHATBOT ⟡           ║
        ║                                                       ║
        ║    Distributed Hash Table Theory & Implementation    ║
        ║                                                       ║
        ╚═══════════════════════════════════════════════════════╝
        """
        
        self.console.print(Align.center(
            Text(banner_text, style="bold cyan")
        ))
        
        info_panel = Panel(
            Text(
                "🔗 Ask questions about Chord DHT theory and project implementation\n"
                "💡 Get detailed technical responses with code references\n"
                "📚 Type 'help' for commands | 'exit' to quit",
                style="white"
            ),
            title="[bold magenta]Welcome[/bold magenta]",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(info_panel)
        self.console.print()
        
    def get_system_prompt(self):
        """Return the specialized system prompt for Chord DHT"""
        return """You are a specialized technical assistant for the Chord DHT (Distributed Hash Table) project.

SCOPE - Only answer questions about:
1. **Chord DHT Theory**: Ring-based distributed hash tables, consistent hashing, finger tables, successor/predecessor relationships, key lookup algorithms, node join/leave operations
2. **This Project's Implementation**: 
   - Main.py: ChordInterface class managing the network UI and operations
   - Network.py: Network class handling node coordination, metrics, security, backup/restore, health checks, load balancing
   - Node.py: Individual node implementation with data storage, finger tables, key management, encryption
   - Features: Network visualization, backup/restore, load balancing, authentication tokens, data encryption, health monitoring

CONSTRAINTS:
- REFUSE to answer questions outside Chord DHT theory and this project
- If asked about unrelated topics, respond: "I can only answer questions about Chord DHT theory and this specific project implementation."
- Provide code references from Main.py, Network.py, or Node.py when relevant
- Explain how project features implement Chord DHT concepts
- Do not provide information about other DHT implementations or unrelated technologies

Keep responses focused, technical, and grounded in Chord DHT principles and project code.
Format your response with clear sections and proper markdown formatting for better readability."""

    def send_message(self, user_message):
        """Send message to the chatbot and get response"""
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": user_message}
            ]
            
            response = client.chat_completion(
                messages=messages,
                max_tokens=1500,
                temperature=0.3,
                top_p=0.9
            )
            
            bot_response = response.choices[0].message.content
            self.conversation_history.append({
                "timestamp": datetime.now(),
                "user": user_message,
                "bot": bot_response
            })
            return bot_response
            
        except Exception as e:
            return f"[red]Error:[/red] {str(e)}"
    
    def display_message(self, sender, message, is_loading=False):
        """Display a message in the chat interface"""
        if sender == "user":
            msg_panel = Panel(
                Text(message, style="white"),
                title="[bold green]You[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
        elif sender == "bot":
            msg_panel = Panel(
                Markdown(message) if not is_loading else Spinner("dots", text="[cyan]Chord Assistant is thinking..."),
                title="[bold magenta]⟡ Chord Assistant[/bold magenta]",
                border_style="magenta",
                padding=(1, 2)
            )
        else:
            msg_panel = Panel(
                Text(message, style="yellow"),
                title="[bold yellow]ℹ️ Info[/bold yellow]",
                border_style="yellow",
                padding=(1, 2)
            )
        
        self.console.print(msg_panel)
        self.console.print()
    
    def display_help(self):
        """Display help menu"""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

[bold green]help[/bold green]         - Show this help menu
[bold green]clear[/bold green]        - Clear the conversation history
[bold green]history[/bold green]      - Show conversation history
[bold green]exit[/bold green]         - Exit the chatbot

[bold cyan]Tips:[/bold cyan]
• Ask questions about Chord DHT theory (finger tables, node join/leave, etc.)
• Ask about the project implementation (Network.py, Node.py, Main.py)
• Combine theory and implementation questions for detailed explanations
• The assistant will refuse to answer unrelated questions
        """
        self.display_message("info", help_text)
    
    def display_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            self.display_message("info", "[yellow]No conversation history yet.[/yellow]")
            return
        
        table = Table(title="[bold cyan]Conversation History[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Time", style="cyan")
        table.add_column("Your Question", style="green")
        table.add_column("Response Summary", style="yellow")
        
        for entry in self.conversation_history:
            time_str = entry["timestamp"].strftime("%H:%M:%S")
            user_q = entry["user"][:50] + "..." if len(entry["user"]) > 50 else entry["user"]
            bot_a = entry["bot"][:50] + "..." if len(entry["bot"]) > 50 else entry["bot"]
            table.add_row(time_str, user_q, bot_a)
        
        self.console.print(table)
        self.console.print()
    
    def display_stats(self):
        """Display session statistics"""
        elapsed = datetime.now() - self.session_start
        stats_text = f"""
[bold cyan]Session Statistics[/bold cyan]

• [green]Messages Exchanged:[/green] {len(self.conversation_history)}
• [cyan]Session Duration:[/cyan] {elapsed.seconds // 60} min {elapsed.seconds % 60} sec
• [magenta]Start Time:[/magenta] {self.session_start.strftime("%H:%M:%S")}
        """
        self.display_message("info", stats_text)
    
    def run(self):
        """Main chat loop"""
        self.console.print("[bold cyan]Type your question or 'help' for commands...[/bold cyan]\n")
        
        while True:
            try:
                # Input prompt with styling
                user_input = self.console.input("[bold green]You:[/bold green] ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == "exit":
                    self.display_message("info", "[cyan]Thank you for using Chord DHT Chatbot! Goodbye! 👋[/cyan]")
                    self.display_stats()
                    break
                
                elif user_input.lower() == "help":
                    self.display_help()
                    continue
                
                elif user_input.lower() == "clear":
                    self.conversation_history.clear()
                    os.system("clear" if os.name == "posix" else "cls")
                    self.display_banner()
                    self.display_message("info", "[green]✓ Conversation history cleared![/green]")
                    continue
                
                elif user_input.lower() == "history":
                    self.display_history()
                    continue
                
                # Display user message
                self.display_message("user", user_input)
                
                # Get response with loading spinner
                with self.console.status("[cyan]⟡ Processing...", spinner="dots"):
                    response = self.send_message(user_input)
                
                # Display bot response
                self.display_message("bot", response)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
                continue
            except Exception as e:
                self.display_message("info", f"[red]Error: {str(e)}[/red]")
                continue


def main():
    """Main entry point"""
    chatbot = ChordChatbotGUI()
    chatbot.run()


if __name__ == "__main__":
    main()
