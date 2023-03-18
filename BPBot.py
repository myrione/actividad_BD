import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, PicklePersistence, ConversationHandler
from config import cfg_item
from commands import Commands
from data_gathering import DataGathering


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

commands = Commands()
data = DataGathering()

"""
    Resumen del bot BTC_Pulse
    
    BCT Pulse es un bot informativo para Telegram que ofrece cifras y datos útiles de Bitcoin.
    Por el momento, implementa tres comandos del sistema: el comando 'start' que inicializa el bot y recaba información del nuevo usuario en forma de encuesta guiada y almacena la información en la base de datos SQLite, 'help' que ofrece definiciones de términos empleados para dar la información de Bitcoin, y 'comandos' que incluye una lista de todos los comandos disponibles del bot. Se puede acceder a esta misma lista desde el propio bot, a través del botón con tres rayas de la parte izqueirda del campo de introducción de texto.
    Además, el bot incluye otros cuatro comandos, tres de ellos informativos y uno social. Los comandos informativos son 'fg_index' que muestra una imagen del índice de miedo y codicia actual y envía el histórico de este índice en texto. 'On-chain' muestra indicadores de la cadena de bloques en formato texto, e 'Info_mercado' ofrece la información actual del mercado en la divisa que escoja el usuario por medio del Inline keyboard implementado. La función social 'sentimiento' traduce la variación diaria y semanal del precio de Bitcoin en un GIF que transmite el sentimiento correspondiente a esa variación.
    
"""

def main() -> None:
       
    print("BOT RUNNING, PRESS CTRL-C TO EXIT!!!")
    persistence = PicklePersistence(filepath="conversationbot")
    application = Application.builder().token(cfg_item('bot', 'token')).persistence(persistence).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", data.start)],                                    
        states={ 
            data.GENDER: [
                CallbackQueryHandler(data.get_gender)  
            ],
            data.AGE: [
                CallbackQueryHandler(data.get_age)
            ],
            data.KNOWLEDGE: [
                CallbackQueryHandler(data.get_knowledge)
            ],
            data.EDUCATION: [
                CallbackQueryHandler(data.get_education)
            ],
            data.INCOME: [
                CallbackQueryHandler(data.get_income)
            ],
        },        
        fallbacks=[MessageHandler(filters.Regex("^Salir$"), data.END)],
        name="data_gathering",
    )

    application.add_handler(conv_handler)

    #application.add_handler(CommandHandler("start", conv_handler))
    application.add_handler(CommandHandler("comandos", commands.commands))
    application.add_handler(CommandHandler("help", commands.help))
    application.add_handler(CommandHandler("fg_index", commands.fear_greed_index))
    application.add_handler(CommandHandler("on_chain", commands.on_chain_indicators))
    application.add_handler(CommandHandler("info_mercado", commands.market_stats))
    application.add_handler(CommandHandler("sentimiento", commands.feeling))
    
    application.add_handler(CallbackQueryHandler(commands.currency_button))
    application.add_handler(MessageHandler(filters.COMMAND, commands.unknown))
    
    
    application.run_polling()

if __name__ == "__main__":
    main()