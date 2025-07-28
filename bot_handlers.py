import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from verb_engine import VerbEngine
from config import WELCOME_MESSAGE, HELP_MESSAGE, TENSE_GROUPS

# Initialize the verb engine
verb_engine = VerbEngine()

# Store current challenges and practice sessions for each user
user_challenges = {}
user_practice_sessions = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    await update.message.reply_text(HELP_MESSAGE)

async def practice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /practice command - show tense group selection."""
    user_id = update.effective_user.id
    
    # Initialize user selection if not exists
    if user_id not in user_practice_sessions:
        user_practice_sessions[user_id] = {
            'selected_groups': [],
            'active': False
        }
    else:
        user_practice_sessions[user_id]['selected_groups'] = []
        user_practice_sessions[user_id]['active'] = False
    
    await show_tense_selection(update.message, user_id)

async def show_tense_selection(message_obj, user_id):
    """Show tense group selection with checkboxes."""
    selected_groups = user_practice_sessions[user_id]['selected_groups']
    
    # Create inline keyboard for tense group selection
    keyboard = []
    for group_key, group_info in TENSE_GROUPS.items():
        if group_key == 'all':
            continue  # Skip 'all' option for now
        
        # Add checkmark if selected
        prefix = "✅ " if group_key in selected_groups else "☐ "
        keyboard.append([InlineKeyboardButton(
            f"{prefix}{group_info['name_es']}", 
            callback_data=f"toggle_{group_key}"
        )])
    
    # Add control buttons
    keyboard.append([
        InlineKeyboardButton("🎯 Empezar práctica", callback_data="start_practice"),
        InlineKeyboardButton("🔄 Resetear", callback_data="reset_selection")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    selected_text = ", ".join([TENSE_GROUPS[g]['name_es'] for g in selected_groups]) if selected_groups else "Nada seleccionado"
    
    message = "🎯 **Selecciona tiempos para practicar:**\n\n"
    message += f"Seleccionado: {selected_text}\n\n"
    message += "Haz clic en los tiempos para seleccionar/deseleccionar, luego 'Empezar práctica'"
    
    await message_obj.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_tense_group_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle tense group selection from inline keyboard."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    if data == "stop_practice":
        # Stop practice session
        if user_id in user_practice_sessions:
            del user_practice_sessions[user_id]
        if user_id in user_challenges:
            del user_challenges[user_id]
        
        await query.edit_message_text("🛑 Práctica detenida. Usa /practice para empezar de nuevo.")
        return
    
    if data.startswith("toggle_"):
        # Toggle tense group selection
        group_key = data.replace("toggle_", "")
        selected_groups = user_practice_sessions[user_id]['selected_groups']
        
        if group_key in selected_groups:
            selected_groups.remove(group_key)
        else:
            selected_groups.append(group_key)
        
        # Update the selection display
        await update_tense_selection(query, user_id)
        
    elif data == "start_practice":
        # Start practice with selected groups
        selected_groups = user_practice_sessions[user_id]['selected_groups']
        
        if not selected_groups:
            await query.answer("¡Selecciona al menos un grupo de tiempos!", show_alert=True)
            return
        
        # Start practice session
        user_practice_sessions[user_id]['active'] = True
        user_practice_sessions[user_id]['selected_groups'] = selected_groups
        
        # Generate first challenge
        await generate_challenge_for_groups(query, user_id, selected_groups)
        
    elif data == "reset_selection":
        # Reset selection
        user_practice_sessions[user_id]['selected_groups'] = []
        await update_tense_selection(query, user_id)

async def update_tense_selection(query, user_id):
    """Update the tense selection message."""
    selected_groups = user_practice_sessions[user_id]['selected_groups']
    
    # Create inline keyboard for tense group selection
    keyboard = []
    for group_key, group_info in TENSE_GROUPS.items():
        if group_key == 'all':
            continue  # Skip 'all' option for now
        
        # Add checkmark if selected
        prefix = "✅ " if group_key in selected_groups else "☐ "
        keyboard.append([InlineKeyboardButton(
            f"{prefix}{group_info['name_es']}", 
            callback_data=f"toggle_{group_key}"
        )])
    
    # Add control buttons
    keyboard.append([
        InlineKeyboardButton("🎯 Empezar práctica", callback_data="start_practice"),
        InlineKeyboardButton("🔄 Resetear", callback_data="reset_selection")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    selected_text = ", ".join([TENSE_GROUPS[g]['name_es'] for g in selected_groups]) if selected_groups else "Nada seleccionado"
    
    message = "🎯 **Selecciona tiempos para practicar:**\n\n"
    message += f"Seleccionado: {selected_text}\n\n"
    message += "Haz clic en los tiempos para seleccionar/deseleccionar, luego 'Empezar práctica'"
    
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')

async def generate_challenge_for_groups(query_or_update, user_id, tense_groups):
    """Generate a new challenge for the specified tense groups."""
    challenge = verb_engine.get_random_challenge_by_groups(tense_groups)
    user_challenges[user_id] = challenge
    
    # Create the challenge message with only verb translation
    message = f"🔤 **Conjugar el verbo:**\n\n"
    message += f"**{challenge['verb']}** ({challenge['verb_translation']}) "
    message += f"en **{challenge['tense_display']}** "
    message += f"para **{challenge['person']}**\n\n"
    message += f"Escribe tu respuesta:"
    
    # Create inline keyboard for stopping practice
    keyboard = [[InlineKeyboardButton("🛑 Parar práctica", callback_data="stop_practice")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(query_or_update, 'edit_message_text'):
        # This is a callback query
        await query_or_update.edit_message_text(message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        # This is a regular update
        await query_or_update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages (answers to challenges)."""
    user_id = update.effective_user.id
    user_answer = update.message.text.strip()
    
    # Check if user has an active challenge
    if user_id not in user_challenges:
        await update.message.reply_text(
            "¡Hola! 👋 Usa /practice para empezar a practicar conjugaciones de verbos."
        )
        return
    
    challenge = user_challenges[user_id]
    correct_answer = challenge['correct_answer']
    
    # Check if the answer is correct
    is_correct = verb_engine.check_answer(user_answer, correct_answer)
    
    # Check if user has an active practice session
    has_active_session = user_id in user_practice_sessions and user_practice_sessions[user_id]['active']
    
    if is_correct:
        # Correct answer
        response = f"¡Correcto! ✅\n\n"
        response += f"**{challenge['verb']}** ({challenge.get('verb_translation', challenge['verb'])}) → **{correct_answer}**\n\n"
        
        # Clear the current challenge
        del user_challenges[user_id]
        
        if has_active_session:
            # Continue with next challenge in the same groups
            response += f"Siguiente pregunta:"
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Generate next challenge
            selected_groups = user_practice_sessions[user_id]['selected_groups']
            await generate_challenge_for_groups(update, user_id, selected_groups)
        else:
            response += f"¿Quieres practicar otro verbo? Usa /practice"
            await update.message.reply_text(response, parse_mode='Markdown')
    else:
        # Incorrect answer
        response = f"❌ Incorrecto.\n\n"
        response += f"Tu respuesta: **{user_answer}**\n"
        response += f"Respuesta correcta: **{correct_answer}**\n\n"
        
        # Clear the current challenge
        del user_challenges[user_id]
        
        if has_active_session:
            # Continue with next challenge in the same groups
            response += f"Siguiente pregunta:"
            await update.message.reply_text(response, parse_mode='Markdown')
            
            # Generate next challenge
            selected_groups = user_practice_sessions[user_id]['selected_groups']
            await generate_challenge_for_groups(update, user_id, selected_groups)
        else:
            response += f"¿Quieres intentar otro verbo? Usa /practice"
            await update.message.reply_text(response, parse_mode='Markdown')

async def handle_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle continuation requests after a correct answer."""
    user_id = update.effective_user.id
    
    # If user doesn't have an active challenge, start a new one
    if user_id not in user_challenges:
        await practice_command(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logging.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "¡Ups! Algo salió mal. Intenta de nuevo con /practice"
        )
