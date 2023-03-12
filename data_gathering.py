import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Dict


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class DataGathering:
    
    GENDER, AGE, KNOWLEDGE, EDUCATION, INCOME, NATIONALITY, CURRENT_LEVEL, SHOW_DATA, START_OVER, END = map(chr, range(10))
    
    def __init__(self):
        
        self.current_state = self.GENDER
        self.data = {}
        
        self.__gender_buttons = [
            [InlineKeyboardButton("Hombre", callback_data="Hombre"),
            InlineKeyboardButton("Mujer", callback_data="Mujer"),
            ],
            ]
        self.__age_buttons = [
            [InlineKeyboardButton("15-20", callback_data="15-20"),
            InlineKeyboardButton("20-30", callback_data="20-30"),
            InlineKeyboardButton("30-40", callback_data="30-40"),
            InlineKeyboardButton("40-50", callback_data="40-50"),
            InlineKeyboardButton(">50", callback_data=">50"),
            ],
        ]
        self.__knowledge_buttons = [
            [InlineKeyboardButton("Principiante", callback_data="Principiante"),
            InlineKeyboardButton("Intermedio", callback_data="Intermedio"),
            InlineKeyboardButton("Avanzado", callback_data="Avanzado"),
            InlineKeyboardButton("Hodlr a muerte", callback_data="Hodlr"),
            ],
            ]
        self.__education_buttons = [
            [InlineKeyboardButton("Sin estudios", callback_data="Sin_estudios"),
            InlineKeyboardButton("Secundaria", callback_data="Secundaria"),
            InlineKeyboardButton("Formación profesional", callback_data="Formación_profesional"),
            InlineKeyboardButton("Estudios universitarios", callback_data="Estudios_universitarios"),
            InlineKeyboardButton("Máster y postgrado", callback_data="Máster_postgrado"),
            InlineKeyboardButton("Doctorado", callback_data="Doctorado"),
            ],
        ]
        self.__income_buttons = [
            [InlineKeyboardButton("Sin ingresos regulares", callback_data="Sin_ingresos_regulares"),
            InlineKeyboardButton("<10.000 €/$", callback_data="<10.000"),
            InlineKeyboardButton("10-15.000 €/$", callback_data="10-15.000"),
            InlineKeyboardButton("15-25.000 €/$", callback_data="15-25.000"),
            InlineKeyboardButton("25-35.000 €/$", callback_data="25-35.000"),
            InlineKeyboardButton("35-45.000 €/$", callback_data="35-45.000"),
            InlineKeyboardButton("<45.000 €/$", callback_data="<45.000"),
            ]
        ]
           
   
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE, ) -> None:
        """
        Este comando da la bienvenida y explica la finalidad del bot. Además, solicita información del usuario, que usuario introduce pulsando los diferentes botones que se muestran en pantalla.
        También se almacena el usuario de Telegram y el Id en la BD."""
        
        info_request_text = ("Para empezar, me gustaría saber algunas cosas sobre ti, porque así podré ofrecerte información más personalizada y tener más conocimientos sobre esta comunidad de bitcoiners. No tienes que responder si no quieres, no es obligatorio.")
                             
        first_question = ("Empecemos por tu género: escoge el tuyo.")
         
        keyboard = InlineKeyboardMarkup(self.__gender_buttons)
        
        #comprueba el usuario y lo guarda
        # user_id = update.effective_user
        user_name = update.effective_user
        # DBHelper.check_user(update, user_id)
        
        #guarda el género seleccionado en la BD
        # category = context.user_data[DataGathering.SELECTING_GENDER]
        # text = update.callback_query
        # await text.answer()
        # DBHelper.update_user(category, text.data, update)
                
        await update.message.reply_text(
            rf"""¡Hola, bienvenid@ bitcoiner!
            Estoy aquí para darte <u>información</u> valiosa sobre Bitoin para ayudarte a hacer un seguimiento y a tomar mejores decisiones de compra, venta y acumulación. Utiliza <b>/comandos</b> para ver los comandos disponibles y la información que contienen, y <b>/help</b> para obtener ayuda sobre la terminología empleada. 
            """
            )
        await update.message.reply_text(text=info_request_text+first_question, parse_mode='HTML', reply_markup=keyboard)
        
        
        return DataGathering.GENDER
    
    async def select_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        
        level = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = level
        query = update.callback_query
        self.data["gender"] = query.data
        message = "Ok. Ahora, selecciona tu edad entre estos rangos."
        
        keyboard = InlineKeyboardMarkup(self.__age_buttons)
        
        # category = context.user_data[self.AGE]
        # text = update.callback_query
        # await text.answer()
        # DBHelper.update_user(category, text, update)
        self.current_state = DataGathering.AGE
        
        await update.callback_query.answer()
        await query.message.reply_text(text=message, reply_markup=keyboard)

        
        return DataGathering.AGE
    
    async def select_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        level = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = level
        message = "Ok. Ahora, selecciona tu nivel de conocimientos sobre Bitcoin."
        query = update.callback_query
        self.data["age"] = query.data
        
        keyboard = InlineKeyboardMarkup(self.__knowledge_buttons)
        
        # category = context.user_data[self.KNOWLEDGE]
        # text = update.callback_query
        # await text.answer()
        # DBHelper.update_user(category, text, update)

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = DataGathering.KNOWLEDGE
        return DataGathering.KNOWLEDGE
   
    async def select_knowledge(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        level = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = level
    
        query = update.callback_query
        self.data["knowledge"] = query.data
        message = "Ok. ahora, selecciona tu nivel de estudios."
        
        keyboard = InlineKeyboardMarkup(self.__education_buttons)
        
        # category = context.user_data[self.EDUCATION]
        # text = update.callback_query
        # await text.answer()
        # DBHelper.update_user(category, text, update)

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = DataGathering.EDUCATION
        return DataGathering.EDUCATION
    
    async def select_education(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        level = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = level
        
        query = update.callback_query
        self.data["education"] = query.data
        
        message = "Ok. ahora, selecciona tu nivel de ingresos anuales:"
        
        keyboard = InlineKeyboardMarkup(self.__income_buttons)
        
        # category = context.user_data[self.INCOME]
        # text = int(update.callback_query)
        # await text.answer()
        # DBHelper.update_user(category, text, update)

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = self.INCOME
        return self.INCOME
    
    async def select_income(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        level = update.callback_query.data
        context.user_data[self.CURRENT_LEVEL] = level
        
        query = update.callback_query
        self.data["income"] = query.data
        
        message = "Ok. Por último, escribe tu nacionalidad."
               
        # category = context.user_data[self.NATIONALITY]
        # text = update.message.text
        # await text.answer()
        # DBHelper.update_user(category, text, update)

        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=message)

        self.current_state = self.NATIONALITY
        return self.NATIONALITY 

    async def save_nationality(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        level = update.callback_query.data
        context.user_data[self.CURRENT_LEVEL] = level
        
        message = "Ok. ¡Eso es todo! Muchas gracias por la información, y espero servirte de ayuda. Escribe <b>/comandos</b> para ver lo que puedo hacer por ti. También puedes acceder a mis funciones con el botón de tres rayas de la parte izquierda del campo de introducción de texto."
        
        # category = context.user_data[self.NATIONALITY]
        # text = update.message.text
        # await text.answer()
        # DBHelper.update_user(category, text, update)
        user_data = context.user_data
        user_data[self.NATIONALITY] = update.message.text
        
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=message)

        self.current_state = self.END
        return self.END
    

