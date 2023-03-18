import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from typing import Dict
from dbhelper import DBHelper


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class DataGathering:
    
    GENDER, AGE, KNOWLEDGE, EDUCATION, INCOME, CURRENT_LEVEL, END = map(chr, range(7))
    
    def __init__(self):
        
        self.__DB = DBHelper()
        self.current_state = {}
        self.data = {}
        self.__gender_buttons = [
            [InlineKeyboardButton("Hombre", callback_data="Hombre"),
            InlineKeyboardButton("Mujer", callback_data="Mujer"),
            ],
            ]
        self.__age_buttons = [
            [InlineKeyboardButton("15-20", callback_data="15-20"),
            InlineKeyboardButton("20-30", callback_data="20-30")],
            [InlineKeyboardButton("30-40", callback_data="30-40"),
            InlineKeyboardButton("40-50", callback_data="40-50"),
            InlineKeyboardButton(">50", callback_data=">50")],
        ]
        self.__knowledge_buttons = [
            [InlineKeyboardButton("Principiante", callback_data="Principiante"),
            InlineKeyboardButton("Intermedio", callback_data="Intermedio")],
            [InlineKeyboardButton("Avanzado", callback_data="Avanzado"),
            InlineKeyboardButton("Hodlr a muerte", callback_data="Hodlr")],
            ]
        self.__education_buttons = [
            [InlineKeyboardButton("Sin estudios", callback_data="Sin estudios"),
            InlineKeyboardButton("Secundaria", callback_data="Secundaria")],
            [InlineKeyboardButton("Formación profesional", callback_data="Formación profesional"),
            InlineKeyboardButton("Estudios universitarios", callback_data="Estudios_universitarios")],
            [InlineKeyboardButton("Máster y postgrado", callback_data="Máster y/o postgrado"),
            InlineKeyboardButton("Doctorado", callback_data="Doctorado"),
            ], 
        ]
        self.__income_buttons = [
            [InlineKeyboardButton("Sin ingresos regulares", callback_data="Sin_ingresos_regulares"),
            InlineKeyboardButton("<10.000", callback_data="<10.000")],
            [InlineKeyboardButton("10-15.000", callback_data="10-15.000"),
            InlineKeyboardButton("15-25.000", callback_data="15-25.000"),
            InlineKeyboardButton("25-35.000", callback_data="25-35.000")],
            [InlineKeyboardButton("35-45.000", callback_data="35-45.000"),
            InlineKeyboardButton("<45.000", callback_data="<45.000"),
            ]
        ]
       
 
       
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """
        Este comando da la bienvenida y explica la finalidad del bot. Además, solicita información del usuario, que usuario introduce pulsando los diferentes botones que se muestran en pantalla.
        También se almacena el usuario de Telegram y el Id en la BD."""
        
        info_request_text = ("Para empezar, me gustaría saber algunas cosas sobre ti, porque así podré ofrecerte información más personalizada y tener más conocimientos sobre esta comunidad de bitcoiners. No tienes que responder si no quieres, no es obligatorio.")
                             
        first_question = ("Empecemos por tu género: escoge el tuyo.")
         
        keyboard = InlineKeyboardMarkup(self.__gender_buttons)
        
        #crea la tabla, comprueba el usuario y lo guarda
        self.__DB.execute_query()
        #user_data = update.effective_user
        self.__DB.check_user(update, self.data)
        
        
        # category = context.user_data[DataGathering.SELECTING_GENDER]
        
        
        # DBHelper.update_user(category, text.data, update)
        user = update.effective_user
        await update.message.reply_html(
            rf"""¡Hola, {user.mention_html()}, bienvenid@ bitcoiner!
            Estoy aquí para darte <u>información</u> valiosa sobre Bitcoin para ayudarte a hacer un seguimiento y a tomar mejores decisiones de compra, venta y acumulación. Utiliza <b>/comandos</b> para ver los comandos disponibles y la información que contienen, y <b>/help</b> para obtener ayuda sobre la terminología empleada. 
            """
            )
        await update.message.reply_html(text=info_request_text+first_question, reply_markup=keyboard)
        
    
        return self.GENDER
    
    async def get_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        
        gender = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = DataGathering.GENDER
        self.data["Genero"] = gender
        message = "Ok. Ahora, selecciona tu edad entre estos rangos."
        keyboard = InlineKeyboardMarkup(self.__age_buttons)
        
        #guarda el género
        category = "Genero"
        text = gender
        self.__DB.update_user(category, text, update.callback_query.from_user.id)

        await update.callback_query.message.reply_text(text=message, reply_markup=keyboard)        
        
        self.current_state = DataGathering.AGE
        return DataGathering.AGE
    
    async def get_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        age = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = DataGathering.AGE
        self.data["Edad"] = age
        message = "Ok. Ahora, selecciona tu nivel de conocimientos sobre Bitcoin."
        keyboard = InlineKeyboardMarkup(self.__knowledge_buttons)
        
        #guarda la edad
        category = "Edad"
        text = age
        self.__DB.update_user(category, text, update.callback_query.from_user.id)

        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = DataGathering.KNOWLEDGE
        return DataGathering.KNOWLEDGE
   
    async def get_knowledge(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        knowledge = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = DataGathering.KNOWLEDGE
        self.data["Conocimientos"] = knowledge
        message = "Ok. ahora, selecciona tu nivel de estudios."
        keyboard = InlineKeyboardMarkup(self.__education_buttons)
        
        #guarda el nivel de conocimientos
        category = "Conocimientos"
        text = knowledge
        self.__DB.update_user(category, text, update.callback_query.from_user.id)

        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = DataGathering.EDUCATION
        return DataGathering.EDUCATION
    
    async def get_education(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        education = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = DataGathering.EDUCATION
        self.data["Nivel de estudios"] = education
        message = "Ok. ahora, selecciona tu nivel de ingresos anuales:"
        keyboard = InlineKeyboardMarkup(self.__income_buttons)
        
        #guarda el nivel de estudios
        category = "Estudios"
        text = education
        self.__DB.update_user(category, text, update.callback_query.from_user.id)
        
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)

        self.current_state = DataGathering.INCOME
        return self.INCOME


    async def get_income(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:

        income = update.callback_query.data
        context.user_data[DataGathering.CURRENT_LEVEL] = DataGathering.INCOME
        self.data["Ingresos"] = income#query.data

        show_data = f"Ok. ¡Eso es todo! Me has proporcionado estos datos sobre ti: {self.facts_to_str(context.user_data)}"
        end_message = f"""Si te has equivocado en algún paso, pulsa <b>/start</b> y vuelve seleccionar tus datos. 
        Escribe <b>/comandos</b> para ver todo lo que puedo hacer por ti. También puedes acceder a mis funciones con el botón de menú de la parte izquierda del campo de introducción de texto."""
               
        #guarda el nivel de ingresos
        category = "Ingresos"
        text = income
        self.__DB.update_user(category, text, update.callback_query.from_user.id)

        await update.callback_query.edit_message_text(show_data+end_message, parse_mode='HTML')

        self.data.clear()
        self.__DB.connection.close()
        return ConversationHandler.END
    
    def facts_to_str(self, user_data: Dict[str, str]) -> str:
        """Función para dar formato los datos recabados."""
        facts = [f"<b>{key}</b> - {value}" for key, value in self.data.items()]
        return "\n".join(facts).join(["\n", "\n"])



