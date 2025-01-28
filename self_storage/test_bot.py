from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
import sys
import datetime
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()
# Настройки
API_TOKEN = '7059249621:AAESH12pz_Ug5u2hy0nKFBXgNudpcv7eNPc'

# Логирование
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Бот и диспетчер
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router(name="main_router")
scheduler = AsyncIOScheduler()

# Модели Django
from storage.models import Order, Client, Cell


def save_order_to_db(tg_id, address, phone_number, cell_id, start_date, end_date):
    try:
        client, _ = Client.objects.get_or_create(tg_id=tg_id, defaults={'client_name': f'User_{tg_id}'})
    except Client.DoesNotExist:
        raise ValueError("Клиент не найден")

    try:
        cell = Cell.objects.get(id=cell_id)
    except Cell.DoesNotExist:
        raise ValueError("Ячейка не найдена")

    order = Order(
        client=client,
        contacts=phone_number,
        start_storage=start_date,
        end_storage=end_date,
        address=address,
        cell=cell
    )
    order.save()

    return order


class OrderStates(StatesGroup):
    WAITING_FOR_ADDRESS = State()
    WAITING_FOR_PHONE_NUMBER = State()


# Приветственное сообщение
@router.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Вот несколько примеров, когда аренда склада может вам пригодиться:\n\n"
                        "- Хранение сезонных вещей (лыжи, велосипеды)\n"
                        "- Временное хранение мебели при переезде\n"
                        "- Хранение документов и архивов\n\n"
                        "Что бы вы хотите сделать?")


# Правила хранения и список разрешенных/запрещенных вещей
@router.message(F.text("правила"))
async def show_rules(message: types.Message):
    await message.reply("Вот наши правила хранения и список разрешенных/запрещенных вещей:\n\n"
                        "Разрешено:\n"
                        "- Одежда\n"
                        "- Мебель\n"
                        "- Спортивное оборудование\n\n"
                        "Запрещено:\n"
                        "- Легковоспламеняющиеся вещества\n"
                        "- Опасные химические вещества\n"
                        "- Продукты питания\n\n")


# Начало процесса заказа бокса
@router.message(F.text("заказать бокс"))
async def start_order_process(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    button_delivery = types.InlineKeyboardButton(text="Бесплатная доставка из дома", callback_data="delivery")
    button_self_delivery = types.InlineKeyboardButton(text="Самостоятельная доставка", callback_data="self_delivery")
    keyboard.add(button_delivery, button_self_delivery)

    await message.answer("Выберите вариант доставки:", reply_markup=keyboard)


# Обработка выбора варианта доставки
@router.callback_query(F.data == "delivery")
async def process_delivery(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text("Пожалуйста, предоставьте ваш адрес:")
    await state.set_state(OrderStates.WAITING_FOR_ADDRESS)


# Получение адреса пользователя
@router.message(OrderStates.WAITING_FOR_ADDRESS)
async def get_address(message: types.Message, state: FSMContext):
    user_address = message.text
    await state.update_data(address=user_address)
    await message.reply("Теперь, пожалуйста, укажите ваш контактный телефон:")
    await state.set_state(OrderStates.WAITING_FOR_PHONE_NUMBER)


# Получение номера телефона пользователя
@router.message(OrderStates.WAITING_FOR_PHONE_NUMBER)
async def get_phone_number(message: types.Message, state: FSMContext):
    user_phone = message.text
    data = await state.get_data()
    address = data['address']
    cell_id = data.get('cell_id')  # Получаем ID ячейки из состояния

    # Сохраняем данные заказа в базу данных
    try:
        order = save_order_to_db(message.from_user.id, address, user_phone, cell_id, start_date, end_date)
    except Exception as e:
        await message.reply(f"Произошла ошибка при создании заказа: {e}")
    else:
        await state.clear()
        await message.reply("Ваш заказ принят! Мы свяжемся с вами для уточнения деталей.")


# Отправка напоминания о завершении срока аренды
async def send_reminder(client_id, days_left):
    client = Client.objects.get(id=client_id)
    await bot.send_message(client.tg_id,
                           f"У вас осталось {days_left} дней до окончания срока аренды. Пожалуйста, заберите свои вещи вовремя.")


# Проверка сроков аренды и отправка напоминаний
async def check_rental_terms():
    current_time = datetime.datetime.now()

    for order in Order.objects.filter(end_storage__gte=current_time,
                                      end_storage__lte=current_time + datetime.timedelta(days=30)):
        days_left = (order.end_storage - current_time).days

        if days_left == 30 or days_left == 14 or days_left == 7 or days_left == 3:
            await send_reminder(order.client.id, days_left)


# Запуск планировщика и старта бота
async def main():
    scheduler.add_job(check_rental_terms, "interval", hours=1)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())