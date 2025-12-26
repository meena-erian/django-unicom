# Interactive menu tool - demonstrates Telegram button functionality
from unicom.services.telegram.create_inline_keyboard import (
    create_inline_keyboard, create_callback_button, create_url_button, create_simple_keyboard
)

def interactive_menu(menu_type: str = "main") -> str:
    """
    Display an interactive menu with buttons for different actions.

    Args:
        menu_type: Type of menu to display ("main", "tools", "info")

    Returns:
        String confirmation that menu was sent
    """
    try:
        # message is available directly as a context variable in tool code
        if not message:
            return "Message context not available"

        # Get the account (recipient of the message)
        account = message.sender if not message.is_outgoing else message.chat.accounts.first()

        # We need to use the incoming message as the reference for buttons
        # since we can't create buttons referencing a message that doesn't exist yet

        if menu_type == "main":
            # Use the incoming message for button callbacks
            message.reply_with({
                "text": "🏠 **Main Menu**\n\nChoose an option below:",
                "reply_markup": create_inline_keyboard([
                    [create_callback_button("🛠️ Tools Menu", {"menu": "tools"}, message=message, account=account)],
                    [create_callback_button("ℹ️ System Info", {"menu": "info"}, message=message, account=account)],
                    [create_callback_button("🎲 Random Fact", {"action": "random_fact"}, message=message, account=account)],
                    [create_url_button("📖 Documentation", "https://github.com/meena-erian/django-unicom")]
                ])
            })
            return "Interactive main menu sent with buttons!"

        elif menu_type == "tools":
            message.reply_with({
                "text": "🛠️ **Tools Menu**\n\nSelect a tool to use:",
                "reply_markup": create_inline_keyboard([
                    [create_callback_button("⏰ Start Timer", {"action": "timer"}, message=message, account=account)],
                    [create_callback_button("🌐 IP Lookup", {"action": "ip_lookup"}, message=message, account=account)],
                    [create_callback_button("📊 System Stats", {"action": "system_info"}, message=message, account=account)],
                    [create_callback_button("🔙 Back to Main", {"menu": "main"}, message=message, account=account)]
                ])
            })
            return "Tools menu sent with buttons!"

        elif menu_type == "info":
            message.reply_with({
                "text": "ℹ️ **Information Menu**\n\nWhat would you like to know?",
                "reply_markup": create_inline_keyboard([
                    [create_callback_button("💻 System Info", {"action": "system_info"}, message=message, account=account)],
                    [create_callback_button("📈 Performance", {"action": "performance"}, message=message, account=account)],
                    [create_callback_button("🔙 Back to Main", {"menu": "main"}, message=message, account=account)]
                ])
            })
            return "Info menu sent with buttons!"

        else:
            message.reply_with({
                "text": f"Unknown menu type: {menu_type}",
                "reply_markup": create_inline_keyboard([
                    [create_callback_button("🏠 Main Menu", {"menu": "main"}, message=message, account=account)]
                ])
            })
            return f"Unknown menu type: {menu_type} (sent error with menu button)"

    except Exception as e:
        import traceback
        traceback.print_exc()
        if message:
            message.reply_with({"text": f"Menu error: {str(e)}"})
        return f"Menu error: {str(e)}"

tool_definition = {
    "name": "interactive_menu",
    "description": "Display an interactive menu with clickable buttons for various actions",
    "parameters": {
        "menu_type": {
            "type": "string",
            "description": "Type of menu to display",
            "enum": ["main", "tools", "info"],
            "default": "main"
        }
    },
    "run": interactive_menu
}
