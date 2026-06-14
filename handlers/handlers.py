import asyncio
import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile
from aiogram.exceptions import TelegramNetworkError
from keyboards.kb_utils import create_inline_kb
from lexicon.lexicon import LEXICON
#from keyboards.kb_utils import continue_btn1, continue_btn2, continue_btn3

router = Router()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE_DIR / 'videos'
PHOTO_DIR = BASE_DIR / 'photos'
MAX_TELEGRAM_FILE_SIZE = 50 * 1024 * 1024


def get_photo_file(file_name: str) -> FSInputFile:
    return FSInputFile(str(PHOTO_DIR / file_name))


async def send_video(message: Message, file_name: str, reply_markup=None):
    user_id = message.from_user.id
    video_path = VIDEO_DIR / file_name
    if not video_path.exists():
        logger.error('Video file not found: %s for user %s', video_path, user_id)
        await message.answer('Видео не найдено. Проверьте путь к файлу.')
        return

    if video_path.stat().st_size > MAX_TELEGRAM_FILE_SIZE:
        await message.answer(
            'Видео слишком большое для Telegram. Сожмите его до 50 МБ или используйте более короткий файл.'
        )
        return

    logger.info('Sending video %s (%0.2f MB) to user %s', video_path, video_path.stat().st_size / (1024*1024), user_id)
    try:
        await message.answer_video(
            video=FSInputFile(str(video_path)),
            caption='',
            reply_markup=reply_markup,
            request_timeout=300,
            protect_content=True
        )
    except TelegramNetworkError as e:
        logger.exception('TelegramNetworkError while sending video %s to user %s', video_path, user_id)
        await message.answer(f'Ошибка при отправке видео: {e}. Попробуйте позже.')
    except Exception as e:
        logger.exception('Unexpected error while sending video %s to user %s', video_path, user_id)
        await message.answer('Произошла ошибка при отправке видео. Попробуйте позже.')


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    user_id = message.from_user.id
    logger.info('User %s started the bot', user_id)
    await message.answer(
        LEXICON['/start'], disable_web_page_preview=True, protect_content=True)
    await message.answer_photo(
        photo=get_photo_file('photo_2026-06-14_15-00-40.jpg'),
        reply_markup=create_inline_kb(1, 'continue_btn1'),
        protect_content=True
    )

@router.callback_query(F.data == 'continue_btn1')
async def process_continue_btn1_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info('User %s pressed continue_btn1', user_id)
    await callback.answer()
    await callback.message.answer(
        LEXICON['/continue1'], disable_web_page_preview=True, protect_content=True)
    await callback.message.answer_photo(
        photo=get_photo_file('photo_2026-06-14_15-01-32.jpg'),
        reply_markup=create_inline_kb(1, 'continue_btn2'),
        protect_content=True
    )


@router.callback_query(F.data == 'continue_btn2')
async def process_continue_btn2_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info('User %s pressed continue_btn2', user_id)
    await callback.answer()
    await callback.message.answer(
        LEXICON['/continue2'],
        reply_markup=create_inline_kb(1, 'continue_btn3'), protect_content=True
    )


@router.callback_query(F.data == 'continue_btn3')
async def process_continue_btn3_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info('User %s pressed continue_btn3', user_id)
    await callback.answer()
    await callback.message.answer(LEXICON['/continue3'], protect_content=True)
