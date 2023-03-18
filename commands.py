from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
    
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import random
import logging
from typing import Any, Dict, Tuple
from config import cfg_item
from metrics import Metrics
from dbhelper import DBHelper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Commands():
    
    """La clase Commands define los comandos del bot de Telegram, y estos se implementan en el main del bot mediante manejadores de comandos de la librería Python-Telegram-bot. El uso de estos manejadores requiere que los métodos de commands que definen los comandos sean funciones asíncronas que deben ser "awaited". Asimismo, estos métodos requieren siempre los parámetros Update y Context. 
    """

    def __init__(self):
        self.__metrics = Metrics()
        self.__reply_keyboard_currency = [
                [InlineKeyboardButton("USD", callback_data='7'),
                InlineKeyboardButton("EUR", callback_data='8')]      
                ]
        self.__markup_currency = InlineKeyboardMarkup(self.__reply_keyboard_currency)    

    #volver a meter al comando start, que llame a la clase DataGathering

    async def commands(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
        message = """
        Tienes disponibles los siguientes comandos:
        */start*: inicio del bot.
        */help*: explicaciones de los indicadores y la terminología    empleados.
        */comandos*: lista de comandos del bot.
        */fg_index*: índice de miedo y codicia actual e histórico.
        */on_chain*: indicadores informativos de la cadena de bloques.
        */info_mercado*: información de mercado como precio, volumen, etc.
        */sentimiento*: traducción de la variación del precio en gif que expresa el sentimiento.
        """
            
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
        help_message = """
            Terminología relevante:
            <b>Capitalización de mercado</b>: valor total de un activo en el mercado. En el caso de Bitcoin, se calcula multiplicando la cantidad total de monedas existentes (circulante) por el precio unitario actual. Sirve para establecer el tamaño y el posicionamiento de un activo en el mercado. 
            <b>Índice de miedo y codicia</b>: se trata de un índice creado para medir el sentimiento del mercado respecto a un activo en base a 5 criterios: la volatilidad, el momento/volumen de mercado, el dominio, las tendencias y las redes sociales. Nos sirve para tomar mejores decisiones de compra o venta operando en contra del sentimiento del mercado.
            <b>Índice SOPR</b>: el SOPR (relación de beneficio de salida gastada, en español) es un indicador on-chain que mide la ganancia o pérdida agregada en el mercado. Nos permite inferir si las ventas del momento se están realizando a pérdida o ganacia y por tanto determinar si el movimiento actual puede o no modificar la tendencia alcista o bajista de Bitcoin. Cuando el índice está por debajo del valor 1, se considera que está en la mejor zona de compra con objetivo a largo plazo.
            <b>Tasa hash o hashrate</b>: es la unidad de medida de todo el poder computacional de la red de Bitcoin. Su valor numérico se utiliza para expresar la cantidad de operaciones matemáticas que se ejecutan entre todos los mineros de Bitcoin que compiten entre sí por la recompensa. Su importancia como indicador reside en que representa la potencia de una red blockchain y también de su seguridad. Cuanto mayor la tasa de hash, más segura es la red de cadena de bloques, y por tanto, más protegida está frente a ciberataques. Para que un ataque tenga éxito debe superar el número de hashrate de la blockchain. También se usa para inferir si una caída en el precio de Bitcoin puede estar influida por la actividad minera. 
            """
        await update.message.reply_text(help_message, parse_mode='HTML')

    async def fear_greed_index(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        history = self.__metrics.FG_history()
        bot= context.bot
        chat_id=update.effective_chat.id
        caption='Índice de miedo y avaricia de hoy'
    
        FG_history_message = rf"""
        <b>Valores históricos</b>:
        <u>Hoy</u>: {history[0]}
        <u>Ayer</u>: {history[1]}
        <u>Semana pasada</u>: {history[2]}
        <u>Mes pasado</u>: {history[3]}
        """
        #La imagen png es un placeholder. La idea es construir un gráfico similar usando Pandas cuando aprenda.
        await bot.sendPhoto(chat_id, photo=cfg_item("FG", "photo_url"), caption=caption)
    
        await bot.send_message(chat_id, FG_history_message, parse_mode='HTML')
      
    async def on_chain_indicators(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        bot= context.bot
        chat_id=update.effective_chat.id
        weekly_addresses, monthly_addresses = self.__metrics.ative_addresses()
        SOPR = rf"""
                <b>Valores del SOPR semanal</b>: {self.__metrics.SOPR}
                """
        adresses = rf"""<b>Nuevas direcciones en la última semana</b>: {weekly_addresses}.
        <br/><b>Nuevas direcciones en el último mes</b>:  {monthly_addresses}
        """
        hash_rate = rf"""
                <b>Hash rate promedio última semana</b>: {self.__metrics.hash_rate}
                """
        mining_difficulty = rf"""
                <b>Dificultad de minado media última semana</b>: {self.__metrics.avg_week_difficulty}"""
                
        #Los valores del SOPR y el hash rate son placeholders. La idea es mostrar gráficos contra el precio de BTC más adelante, cuando aprenda Pandas.
        #To_do: separar mensajes
        await bot.send_message(chat_id, SOPR, parse_mode='HTML') 
        await bot.send_message(chat_id, adresses, parse_mode='HTML')
        await bot.send_message(chat_id, hash_rate, parse_mode='HTML')
        await bot.send_message(chat_id, mining_difficulty, parse_mode='HTML') 
         
        
        
    async def market_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        await update.message.reply_text("Elige la moneda en la que quieres la información:", reply_markup=self.__markup_currency)
    
    async def currency_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        currency = update.callback_query
        await currency.answer()
                        
        if currency.data == '7':
        
            USD_message = rf"""
                <b>USD</b>
                <u>Precio hoy</u>: {self.__metrics.market_data['data']['1']['quotes']['USD']['price']:,.2f} $
                <u>Volumen 24 h</u>: {self.__metrics.market_data['data']['1']['quotes']['USD']['volume_24h']:,.2f}$
                <u>Capitalización mercado</u>: {self.__metrics.market_data['data']['1']['quotes']['USD']['market_cap']:,.2f}$
                <u>Variación día</u>: {self.__metrics.market_data['data']['1']['quotes']['USD']['percent_change_24h']:,.2f} %
                <u>Variación semana</u>: {self.__metrics.market_data['data']['1']['quotes']['USD']['percent_change_7d']:,.2f} %
              """
            await currency.edit_message_text(text=USD_message, parse_mode='HTML')
            
        if currency.data == '8':          
            EUR_message = rf""" 
                <b>EUR</b>
                <u>Precio hoy</u>: {self.__metrics.market_data['data']['1']['quotes']['EUR']['price']:,.2f} €
                <u>Volumen 24 h</u>: {self.__metrics.market_data['data']['1']['quotes']['EUR']['volume_24h']:,.2f} €
                <u>Capitalización mercado</u>: {self.__metrics.market_data['data']['1']['quotes']['EUR']['market_cap']:,.2f} €
                <u>Variación día</u>: {self.__metrics.market_data['data']['1']['quotes']['EUR']['percent_change_24h']:,.2f} %
                <u>Variación semana</u>: {self.__metrics.market_data['data']['1']['quotes']['EUR']['percent_change_7d']:,.2f} %
                """
            await currency.edit_message_text(text=EUR_message, parse_mode='HTML')

            
    def select_gif(self, param):
        
        ranges = {'to_hell' : range(-100, -3), 'bearish': range(-3, 0), 'lateral': range(0,2), 'bullish': range(2,5), 'to_moon': range(5,100)}
        
        gifs = {'to_hell': dict(cfg_item("gifs", "to_hell")), 'bearish': dict(cfg_item("gifs", "bearish")), 'lateral': dict(cfg_item("gifs", "lateral")), 'bullish': dict(cfg_item("gifs", "bullish")), 'to_moon': dict(cfg_item("gifs", "to_moon"))}
    
        for key, value in ranges.items():
            if int(param) in value:
                return gifs[key][random.choice(list(gifs[key].keys()))]
  
    
                
    async def feeling(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            chat_id=update.effective_chat.id
            bot= context.bot
            market_variance_day = self.__metrics.market_data['data']['1']['quotes']['USD']['percent_change_24h']
            
            market_variance_week = self.__metrics.market_data['data']['1']['quotes']['USD']['percent_change_7d']
            print(market_variance_week)
            
            await bot.sendAnimation(chat_id, animation=self.select_gif(market_variance_day), caption='Sentimiento de hoy:', parse_mode='HTML')
            
            await bot.sendAnimation(chat_id, animation=self.select_gif(market_variance_week), caption='Sentimiento de la semana:', parse_mode='HTML')

                
    async def unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Disculpa, no entiendo ese comando. Consulta los comandos disponibles con /comandos")
         
       
        
        
        


    
    
    

        
        

