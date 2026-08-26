# =========================================================
# ETHIO CAR EQUB BOT
# =========================================================
# ETHIO CAR EQUB - RENDER TEST VERSION 2
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, ADMIN_ID

from database import get_db

from models import User, Payment

from states import RegistrationStates

from keyboards import (
    language_keyboard,
    payment_for_keyboard_am,
    payment_for_keyboard_en,
    payment_for_keyboard_or,
    payment_method_keyboard_am,
    payment_method_keyboard_en,
    payment_method_keyboard_or,
    admin_payment_keyboard,
)

from validation import (
    validate_full_name,
    validate_phone,
    validate_cbe_reference,
    validate_telebirr_reference,
)
from config import (
    BOT_TOKEN,
    ADMIN_ID,
    CBE_ACCOUNT_NAME,
    CBE_ACCOUNT_NUMBER,
    TELEBIRR_ACCOUNT_NAME,
    TELEBIRR_PHONE,
    EQUB_AMOUNT,
    DASHBOARD_URL,
)


# =========================================================
# BOT
# =========================================================

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


# =========================================================
# HELPER
# =========================================================

def get_language(data):
    return data.get("language", "am")


def should_block_transaction_reference(existing_payment, current_user_id):
    if not existing_payment:
        return False

    existing_user_id = getattr(existing_payment, "user_id", None)
    status = str(getattr(existing_payment, "status", "") or "").upper()

    if current_user_id is not None and existing_user_id == current_user_id:
        return status != "REJECTED"

    return True


# =========================================================
# /START
# =========================================================

@dp.message(CommandStart())
async def start_command(
    message: Message,
    state: FSMContext
):

    await state.clear()

    await message.answer(
        "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"
        "ወደ ETHIO CAR EQUB እንኳን በደህና መጡ።\n\n"
        "የቋንቋ ምርጫዎን ይምረጡ።",
        parse_mode="HTML",
        reply_markup=language_keyboard()
    )

    await state.set_state(
        RegistrationStates.language
    )


# =========================================================
# LANGUAGE — AMHARIC
# =========================================================

@dp.callback_query(
    RegistrationStates.language,
    F.data == "lang_am"
)
async def select_amharic(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        language="am"
    )

    await callback.answer()

    await callback.message.edit_text(
        "👋 <b>እንኳን ደህና መጡ።</b>\n\n"
        "ክፍያዎን ለራስዎ ወይም ለሌላ ሰው እየሰጡ ነዎት?",
        parse_mode="HTML",
        reply_markup=payment_for_keyboard_am()
    )

    await state.set_state(
        RegistrationStates.payment_for
    )


# =========================================================
# LANGUAGE — AFAN OROMO
# =========================================================

@dp.callback_query(
    RegistrationStates.language,
    F.data == "lang_or"
)
async def select_oromo(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        language="or"
    )

    await callback.answer()

    await callback.message.edit_text(
        "👋 <b>Akkam bultan!</b>\n\n"
        "Baasii keessan ofii ykn nama biraaaf kaffallaa jirtu?",
        parse_mode="HTML",
        reply_markup=payment_for_keyboard_or()
    )

    await state.set_state(
        RegistrationStates.payment_for
    )


# =========================================================
# PAYMENT FOR — SELF
# =========================================================

@dp.callback_query(
    RegistrationStates.payment_for,
    F.data == "pay_self"
)
async def payment_for_self(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        payment_for="self"
    )

    data = await state.get_data()

    language = get_language(data)

    await callback.answer()

    if language == "am":

        await callback.message.edit_text(
            "👤 <b>ሙሉ ስምዎን ያስገቡ።</b>\n\n"
            "ለምሳሌ፦ አበበ ከበደ\n\n"
            "⚠️ እባክዎ እውነተኛ ሙሉ ስም "
            "ያስገቡ።",
            parse_mode="HTML"
        )

    elif language == "or":

        await callback.message.edit_text(
            "👤 <b>Maqaa guutuu keessan galchaa.</b>\n\n"
            "Fakkeenya: Abbaa Bakkalcha\n\n"
            "⚠️ Maqaa dhugaa guutuu galchaa.",
            parse_mode="HTML"
        )

    else:

        await callback.message.edit_text(
            "👤 <b>Enter your full name.</b>\n\n"
            "Example: Abebe Kebede\n\n"
            "⚠️ Please enter your real full name.",
            parse_mode="HTML"
        )

    await state.set_state(
        RegistrationStates.full_name
    )


# =========================================================
# PAYMENT FOR — OTHER
# =========================================================

@dp.callback_query(
    RegistrationStates.payment_for,
    F.data == "pay_other"
)
async def payment_for_other(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        payment_for="other"
    )

    data = await state.get_data()

    language = get_language(data)

    await callback.answer()

    if language == "am":

        await callback.message.edit_text(
            "👤 <b>የሚመዘገበውን ሰው ሙሉ ስም "
            "ያስገቡ።</b>\n\n"
            "ለምሳሌ፦ አበበ ከበደ\n\n"
            "⚠️ እውነተኛ ሙሉ ስም ያስገቡ።",
            parse_mode="HTML"
        )

    elif language == "or":

        await callback.message.edit_text(
            "👤 <b>Nama galmaa ta’uuf maqaa guutuu galchaa.</b>\n\n"
            "Fakkeenya: Abbaa Bakkalcha\n\n"
            "⚠️ Maqaa dhugaa guutuu galchaa.",
            parse_mode="HTML"
        )

    else:

        await callback.message.edit_text(
            "👤 <b>Enter the full name of the "
            "person being registered.</b>\n\n"
            "Example: Abebe Kebede\n\n"
            "⚠️ Please enter the real full name.",
            parse_mode="HTML"
        )

    await state.set_state(
        RegistrationStates.full_name
    )


# =========================================================
# FULL NAME
# =========================================================

@dp.message(
    RegistrationStates.full_name,
    F.text
)
async def receive_full_name(
    message: Message,
    state: FSMContext
):

    full_name = message.text.strip()

    data = await state.get_data()

    language = get_language(data)

    if not validate_full_name(full_name):

        if language == "am":

            await message.answer(
                "❌ የገባው ስም ትክክል አይደለም።\n\n"
                "እባክዎ እውነተኛ ሙሉ ስምዎን "
                "ያስገቡ።\n\n"
                "ለምሳሌ፦ አበበ ከበደ"
            )

        elif language == "or":

            await message.answer(
                "❌ Maqaan galameen sirrii miti.\n\n"
                "Maqaa dhugaa guutuu keessan galchaa."
            )

        else:

            await message.answer(
                "❌ Invalid name.\n\n"
                "Please enter your real full name."
            )

        return

    await state.update_data(
        full_name=full_name
    )

    if language == "am":

        await message.answer(
            "📱 <b>ስልክ ቁጥርዎን ያስገቡ።</b>\n\n"
            "ለምሳሌ፦\n"
            "0912345678\n"
            "+251912345678\n"
            "0712345678\n\n"
            "Ethio telecom ወይም Safaricom "
            "ስልክ ቁጥር መጠቀም ይችላሉ።",
            parse_mode="HTML"
        )

    elif language == "or":

        await message.answer(
            "📱 <b>Bilbila keessan galchaa.</b>\n\n"
            "Fakkeenya:\n"
            "0912345678\n"
            "+251912345678\n"
            "0712345678\n\n"
            "Lakkoofsa Ethio telecom ykn Safaricom ni fudhatama.",
            parse_mode="HTML"
        )

    else:

        await message.answer(
            "📱 <b>Enter your phone number.</b>\n\n"
            "Examples:\n"
            "0912345678\n"
            "+251912345678\n"
            "0712345678\n\n"
            "Ethio telecom or Safaricom numbers "
            "are accepted.",
            parse_mode="HTML"
        )

    await state.set_state(
        RegistrationStates.phone
    )


# =========================================================
# PHONE
# =========================================================

@dp.message(
    RegistrationStates.phone,
    F.text
)
async def receive_phone(
    message: Message,
    state: FSMContext
):

    phone = message.text.strip()

    data = await state.get_data()

    language = get_language(data)

    if not validate_phone(phone):

        if language == "am":

            await message.answer(
                "❌ የስልክ ቁጥሩ ትክክል አይደለም።\n\n"
                "እባክዎ ትክክለኛ የኢትዮጵያ "
                "ስልክ ቁጥር ያስገቡ።\n\n"
                "ለምሳሌ፦\n"
                "0912345678\n"
                "+251912345678\n"
                "0712345678"
            )

        elif language == "or":

            await message.answer(
                "❌ Lakkoofsi bilbila Itiyoophiyaa sirrii miti.\n\n"
                "Fakkeenya:\n"
                "0912345678\n"
                "+251912345678\n"
                "0712345678"
            )

        else:

            await message.answer(
                "❌ Invalid Ethiopian phone number.\n\n"
                "Examples:\n"
                "0912345678\n"
                "+251912345678\n"
                "0712345678"
            )

        return

    await state.update_data(
        phone=phone
    )

    if language == "am":

        await message.answer(
            "💳 <b>የክፍያ ዘዴዎን ይምረጡ።</b>",
            parse_mode="HTML",
            reply_markup=payment_method_keyboard_am()
        )

    elif language == "or":

        await message.answer(
            "💳 <b>Haala kaffaltii keessan filadhaa.</b>",
            parse_mode="HTML",
            reply_markup=payment_method_keyboard_or()
        )

    else:

        await message.answer(
            "💳 <b>Select your payment method.</b>",
            parse_mode="HTML",
            reply_markup=payment_method_keyboard_en()
        )

    await state.set_state(
        RegistrationStates.payment_method
    )


# =========================================================
# PAYMENT METHOD — CBE
# =========================================================

@dp.callback_query(
    RegistrationStates.payment_method,
    F.data == "payment_cbe"
)
async def select_cbe(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        payment_method="cbe"
    )

    await callback.answer()

    language = get_language(
        await state.get_data()
    )

    if language == "am":

        await callback.message.answer(
            "🏦 <b>CBE BANK</b>\n\n"

            "👤 <b>የሂሳብ ባለቤት</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>የሂሳብ ቁጥር</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>የሚከፈለው መጠን</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "⚠️ እባክዎ ክፍያውን ወደላይ "
            "የተጠቀሰው የCBE ሂሳብ ይፈጽሙ።\n\n"

            "ከክፍያው በኋላ የክፍያ ደረሰኝዎን "
            "ይላኩ።",

            parse_mode="HTML"
        )

    elif language == "or":

        await callback.message.answer(
            "🏦 <b>CBE BANK</b>\n\n"

            "👤 <b>Abbaa herrega</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>Lakk. Herrega</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>Hanga kaffalamu</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "⚠️ Kaffaltii kana karaa armaan olitti ibsamee "
            "CBE herregaa geessii.\n\n"

            "Erga kaffallii xumurtanii, ragaa kaffallii keessan ergaa.",

            parse_mode="HTML"
        )

    else:

        await callback.message.answer(
            "🏦 <b>CBE BANK</b>\n\n"

            "👤 <b>Account Owner</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>Account Number</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>Payment Amount</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "Please make the payment to the "
            "CBE account shown above.\n\n"

            "After completing the payment, "
            "send your payment receipt.",

            parse_mode="HTML"
        )

    await request_receipt(
        callback.message,
        "cbe",
        language
    )

    await state.set_state(
        RegistrationStates.receipt
    )


# =========================================================
# PAYMENT METHOD — TELEBIRR
# =========================================================

@dp.callback_query(
    RegistrationStates.payment_method,
    F.data == "payment_telebirr"
)
async def select_telebirr(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        payment_method="telebirr"
    )

    await callback.answer()

    language = get_language(
        await state.get_data()
    )

    if language == "am":

        await callback.message.answer(
            "📱 <b>TELEBIRR</b>\n\n"

            "👤 <b>የሂሳብ ባለቤት</b>\n"
            f"{TELEBIRR_ACCOUNT_NAME}\n\n"

            "📱 <b>የTelebirr ቁጥር</b>\n"
            f"<code>{TELEBIRR_PHONE}</code>\n\n"

            "💰 <b>የሚከፈለው መጠን</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "⚠️ እባክዎ ክፍያውን ወደላይ "
            "የተጠቀሰው የTelebirr ቁጥር ይፈጽሙ።\n\n"

            "ከክፍያው በኋላ የክፍያ ደረሰኝዎን "
            "ይላኩ።",

            parse_mode="HTML"
        )

    elif language == "or":

        await callback.message.answer(
            "📱 <b>TELEBIRR</b>\n\n"

            "👤 <b>Abbaa herrega</b>\n"
            f"{TELEBIRR_ACCOUNT_NAME}\n\n"

            "📱 <b>Lakk. Telebirr</b>\n"
            f"<code>{TELEBIRR_PHONE}</code>\n\n"

            "💰 <b>Hanga kaffalamu</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "⚠️ Kaffaltii kana karaa armaan olitti ibsamee "
            "Telebirr lakkofsaatti geessii.\n\n"

            "Erga kaffallii xumurtanii, ragaa kaffallii keessan ergaa.",

            parse_mode="HTML"
        )

    else:

        await callback.message.answer(
            "📱 <b>TELEBIRR</b>\n\n"

            "👤 <b>Account Owner</b>\n"
            f"{TELEBIRR_ACCOUNT_NAME}\n\n"

            "📱 <b>Telebirr Number</b>\n"
            f"<code>{TELEBIRR_PHONE}</code>\n\n"

            "💰 <b>Payment Amount</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "Please make the payment to the "
            "Telebirr number shown above.\n\n"

            "After completing the payment, "
            "send your payment receipt.",

            parse_mode="HTML"
        )

    await request_receipt(
        callback.message,
        "telebirr",
        language
    )

    await state.set_state(
        RegistrationStates.receipt
    )


# =========================================================
# PAYMENT METHOD — OTHER BANK → CBE
# =========================================================

@dp.callback_query(
    RegistrationStates.payment_method,
    F.data == "payment_other_bank"
)
async def select_other_bank(
    callback: CallbackQuery,
    state: FSMContext
):

    await state.update_data(
        payment_method="other_bank"
    )

    await callback.answer()

    language = get_language(
        await state.get_data()
    )

    if language == "am":

        await callback.message.answer(
            "🏦 <b>ሌላ ባንክ → CBE</b>\n\n"

            "👤 <b>የCBE ሂሳብ ባለቤት</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>የCBE ሂሳብ ቁጥር</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>የሚከፈለው መጠን</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "ከሌላ ባንክ ወደዚህ CBE ሂሳብ "
            "ክፍያውን ይፈጽሙ።\n\n"

            "ከክፍያው በኋላ የክፍያ ደረሰኝዎን "
            "ይላኩ።",

            parse_mode="HTML"
        )

    elif language == "or":

        await callback.message.answer(
            "🏦 <b>Baankii biroo → CBE</b>\n\n"

            "👤 <b>Abbaa herrega CBE</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>Lakk. Herrega CBE</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>Hanga kaffalamu</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "Baankii biraa irraa CBE herregatti kaffaltii geessii.\n\n"

            "Erga kaffallii xumurtanii, ragaa kaffallii keessan ergaa.",

            parse_mode="HTML"
        )

    else:

        await callback.message.answer(
            "🏦 <b>OTHER BANK → CBE</b>\n\n"

            "👤 <b>CBE Account Owner</b>\n"
            f"{CBE_ACCOUNT_NAME}\n\n"

            "💳 <b>CBE Account Number</b>\n"
            f"<code>{CBE_ACCOUNT_NUMBER}</code>\n\n"

            "💰 <b>Payment Amount</b>\n"
            f"<b>{EQUB_AMOUNT} ETB</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "Make the payment from your other bank "
            "account to the CBE account above.\n\n"

            "After completing the payment, "
            "send your payment receipt.",

            parse_mode="HTML"
        )

    await request_receipt(
        callback.message,
        "other_bank",
        language
    )

    await state.set_state(
        RegistrationStates.receipt
    )


# =========================================================
# REQUEST RECEIPT
# =========================================================

async def request_receipt(
    message: Message,
    payment_method: str,
    language: str
):

    if payment_method == "cbe":

        if language == "or":
            await message.answer(
                "🧾 <b>Ragaa kaffallii CBE ergaa.</b>\n\n"
                "Ragaa bankii sirrii ta’e JPG, PNG ykn PDF keessatti ergaa.\n\n"
                "⚠️ Screenshot ykn fakkii jijjamame hin ergin.",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "🧾 <b>የCBE ክፍያ ደረሰኝዎን ይላኩ።</b>\n\n"
                "ትክክለኛውን የባንክ ደረሰኝ "
                "JPG፣ PNG ወይም PDF መልክ ይላኩ።\n\n"
                "⚠️ Screenshot ወይም የተቀየረ "
                "ምስል አይላኩ።",
                parse_mode="HTML"
            )

    elif payment_method == "telebirr":

        if language == "or":
            await message.answer(
                "🧾 <b>Ragaa kaffallii Telebirr ergaa.</b>\n\n"
                "Ragaa Telebirr sirrii ta’e JPG, PNG ykn PDF keessatti ergaa.\n\n"
                "⚠️ Screenshot ykn fakkii jijjamame hin ergin.",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "🧾 <b>የTelebirr ክፍያ ደረሰኝዎን "
                "ይላኩ።</b>\n\n"
                "ትክክለኛውን የTelebirr ደረሰኝ "
                "JPG፣ PNG ወይም PDF መልክ ይላኩ።\n\n"
                "⚠️ Screenshot ወይም የተቀየረ "
                "ምስል አይላኩ።",
                parse_mode="HTML"
            )

    else:

        if language == "or":
            await message.answer(
                "🧾 <b>Ragaa kaffallii keessan ergaa.</b>\n\n"
                "Ragaa sirrii ta’e JPG, PNG ykn PDF ta’uu qaba.\n\n"
                "⚠️ Ragaa kaffallii dhugaa qofa ergaa.",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "🧾 <b>የክፍያ ደረሰኝዎን ይላኩ።</b>\n\n"
                "JPG፣ PNG ወይም PDF መልክ ይሆናል።\n\n"
                "⚠️ ትክክለኛ የክፍያ ደረሰኝ "
                "ብቻ ይላኩ።",
                parse_mode="HTML"
            )


# =========================================================
# RECEIPT PHOTO
# =========================================================

@dp.message(
    RegistrationStates.receipt,
    F.photo
)
async def receive_receipt_photo(
    message: Message,
    state: FSMContext
):

    photo = message.photo[-1]

    await process_receipt(
        message=message,
        state=state,
        file_id=photo.file_id,
        receipt_type="photo"
    )


# =========================================================
# RECEIPT DOCUMENT
# =========================================================

@dp.message(
    RegistrationStates.receipt,
    F.document
)
async def receive_receipt_document(
    message: Message,
    state: FSMContext
):

    document = message.document

    allowed_types = [
        "application/pdf",
        "image/jpeg",
        "image/png"
    ]

    if document.mime_type not in allowed_types:

        await message.answer(
            "❌ እባክዎ JPG፣ PNG ወይም PDF "
            "የክፍያ ደረሰኝ ይላኩ።"
        )

        return

    await process_receipt(
        message=message,
        state=state,
        file_id=document.file_id,
        receipt_type=document.mime_type
    )


# =========================================================
# PROCESS RECEIPT
# =========================================================

async def process_receipt(
    message: Message,
    state: FSMContext,
    file_id: str,
    receipt_type: str
):

    await state.update_data(
        receipt_file_id=file_id,
        receipt_file_type=receipt_type
    )

    data = await state.get_data()

    language = get_language(data)

    payment_method = data.get(
        "payment_method"
    )

    if payment_method in [
        "cbe",
        "other_bank"
    ]:

        if language == "am":

            await message.answer(
                "🔢 <b>የግብይት መለያ ቁጥርዎን "
                "ያስገቡ።</b>\n\n"
                "የCBE የግብይት መለያ ቁጥር "
                "በFT መጀመር አለበት።\n\n"
                "ለምሳሌ፦ "
                "<code>FT26123ABCDE</code>\n\n"
                "በደረሰኙ ላይ እንደተጻፈው "
                "በትክክል ያስገቡ።",
                parse_mode="HTML"
            )

        elif language == "or":

            await message.answer(
                "🔢 <b>Lakk. eergaa/guyyaa kaffallii keessan galchaa.</b>\n\n"
                "Lakkofsi CBE yeroo jalqabaa FT ta’uu qaba.\n\n"
                "Fakkeenya: <code>FT26123ABCDE</code>",
                parse_mode="HTML"
            )

        else:

            await message.answer(
                "🔢 <b>Enter your Transaction "
                "Reference Number.</b>\n\n"
                "For CBE, the reference must start "
                "with FT.\n\n"
                "Example: "
                "<code>FT26123ABCDE</code>",
                parse_mode="HTML"
            )

    else:

        if language == "am":

            await message.answer(
                "🔢 <b>የTelebirr የግብይት ቁጥርዎን "
                "ያስገቡ።</b>\n\n"
                "10–12 ፊደላት ወይም ቁጥሮች "
                "መሆን አለበት።\n\n"
                "በደረሰኙ ላይ እንደተጻፈው "
                "በትክክል ያስገቡ።",
                parse_mode="HTML"
            )

        elif language == "or":

            await message.answer(
                "🔢 <b>Lakk. eergaa Telebirr keessan galchaa.</b>\n\n"
                "Lakkoofsi 10–12 qubee ykn lakkoofsa ta’uu qaba.",
                parse_mode="HTML"
            )

        else:

            await message.answer(
                "🔢 <b>Enter your Telebirr "
                "Transaction Number.</b>\n\n"
                "It must contain 10–12 "
                "letters or numbers.",
                parse_mode="HTML"
            )

    await state.set_state(
        RegistrationStates.transaction_reference
    )


# =========================================================
# TRANSACTION REFERENCE
# =========================================================

@dp.message(
    RegistrationStates.transaction_reference,
    F.text
)
async def receive_transaction_reference(
    message: Message,
    state: FSMContext
):

    reference = message.text.strip().upper()

    data = await state.get_data()

    language = get_language(data)

    payment_method = data.get(
        "payment_method"
    )

    # =====================================================
    # CBE VALIDATION
    # =====================================================

    if payment_method in [
        "cbe",
        "other_bank"
    ]:

        if not validate_cbe_reference(
            reference
        ):

            if language == "am":

                await message.answer(
                    "❌ ያስገቡት የክፍያ ቁጥር "
                    "ትክክል አይደለም።\n\n"
                    "የCBE የግብይት ቁጥር "
                    "በFT መጀመር አለበት።\n\n"
                    "እባክዎ ደረሰኝዎን ይመልከቱና "
                    "እንደገና ይላኩ።"
                )

            elif language == "or":

                await message.answer(
                    "❌ Lakkofsi kaffallii kana sirrii miti.\n\n"
                    "Lakkofsi CBE FT irraa jalqabu qaba.\n\n"
                    "Ragaa keessan ilaaluudhaan irra deebi’anii galchaa."
                )

            else:

                await message.answer(
                    "❌ Invalid CBE transaction reference.\n\n"
                    "Please check your receipt and "
                    "enter it again."
                )

            return

    # =====================================================
    # TELEBIRR VALIDATION
    # =====================================================

    elif payment_method == "telebirr":

        if not validate_telebirr_reference(
            reference
        ):

            if language == "am":

                await message.answer(
                    "❌ ያስገቡት የTelebirr "
                    "የግብይት ቁጥር ትክክል አይደለም።\n\n"
                    "10–12 ፊደላት ወይም ቁጥሮች "
                    "መሆን አለበት።\n\n"
                    "እባክዎ ደረሰኝዎን ይመልከቱና "
                    "እንደገና ይላኩ።"
                )

            elif language == "or":

                await message.answer(
                    "❌ Lakkofsi Telebirr kana sirrii miti.\n\n"
                    "10–12 qubee ykn lakkoofsa ta’uu qaba.\n\n"
                    "Ragaa keessan ilaaluudhaan irra deebi’anii galchaa."
                )

            else:

                await message.answer(
                    "❌ Invalid Telebirr transaction number.\n\n"
                    "Please check your receipt and "
                    "enter it again."
                )

            return

    else:

        await message.answer(
            "❌ Invalid payment method."
        )

        return

    # =====================================================
    # DATABASE
    # =====================================================

    db = get_db()

    try:

        # -------------------------------------------------
        # FIND USER
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.telegram_id ==
                message.from_user.id
            )
            .first()
        )

        # -------------------------------------------------
        # DUPLICATE TRANSACTION CHECK
        # -------------------------------------------------

        existing_payment = (
            db.query(Payment)
            .filter(
                Payment.transaction_reference ==
                reference
            )
            .first()
        )

        if existing_payment and should_block_transaction_reference(
            existing_payment,
            user.id if user else None,
        ):

            # Only treat as duplicate if the reference exists for another user,
            # or for the same user but the previous submission is not REJECTED.

            if user and existing_payment.user_id == user.id:
                if existing_payment.status and existing_payment.status.upper() == "REJECTED":
                    # allow resubmission by same user after rejection
                    pass
                else:
                    # same user already has pending/approved submission
                    if language == "am":
                        await message.answer(
                            "❌ እርስዎ ይህን መለያ ከዚህ በፊት አስገብተዋል፤ እባክዎ የክፍያ ሁኔታዎን ይመልከቱ።"
                        )
                    elif language == "or":
                        await message.answer(
                            "❌ Lakkoofsa kana duraanii galchitaniittu; maaloo haala kaffallii keessan ilaalaa."
                        )
                    else:
                        await message.answer(
                            "❌ You have already submitted this transaction reference; please check your payment status."
                        )
                    return
            else:
                # different user has submitted this reference: block
                if language == "am":
                    await message.answer(
                        "❌ ይህ የግብይት መለያ ቁጥር ከሌላ ተጠቃሚ የተላከ ነው።\n\n"
                        "እባክዎ ደረሰኝዎን በትክክል ይመልከቱ።"
                    )
                elif language == "or":
                    await message.answer(
                        "❌ Lakkoofsi eergaa kana nama biroo galcheera.\n\n"
                        "Maaloo ragaa keessan sirrii ta’e ilaalaa."
                    )
                else:
                    await message.answer(
                        "❌ This transaction reference was submitted by another user. Please check your receipt or contact an administrator."
                    )
                return

        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        if not user:

            user = User(

                telegram_id=message.from_user.id,

                telegram_username=(
                    message.from_user.username
                    if message.from_user.username
                    else None
                ),

                language=language,

                participant_name=data[
                    "full_name"
                ],

                phone=data[
                    "phone"
                ]
            )

            db.add(user)

            db.flush()

        else:

            user.language = language

            user.participant_name = data[
                "full_name"
            ]

            user.phone = data[
                "phone"
            ]

            db.flush()

        # -------------------------------------------------
        # RECEIPT
        # -------------------------------------------------

        receipt_file_id = data.get(
            "receipt_file_id"
        )

        receipt_file_type = data.get(
            "receipt_file_type"
        )

        if not receipt_file_id:

            await message.answer(
                "❌ ደረሰኙ አልተገኘም።\n\n"
                "እባክዎ /start በመጫን "
                "እንደገና ይጀምሩ።"
            )

            return

        # -------------------------------------------------
        # CREATE PAYMENT
        # -------------------------------------------------

        if existing_payment:

            payment = existing_payment

            payment.user_id = user.id

            payment.payment_method = payment_method

            payment.receipt_path = receipt_file_id

            payment.transaction_reference = reference

            payment.payment_for = data.get("payment_for")

            payment.participant_name = (
                data.get("full_name") or user.participant_name
            )

            payment.participant_phone = (
                data.get("phone") or user.phone
            )

            payment.participant_number = None

            payment.status = "PENDING"

            payment.verified_at = None

            payment.rejection_reason = None

        else:

            payment = Payment(

                user_id=user.id,

                payment_method=payment_method,

                receipt_path=receipt_file_id,

                transaction_reference=reference,

                payment_for=data.get("payment_for"),

                participant_name=(
                    data.get("full_name") or user.participant_name
                ),

                participant_phone=(
                    data.get("phone") or user.phone
                ),

                status="PENDING"
            )

            db.add(payment)

        db.commit()

        db.refresh(payment)

        payment_id = payment.id

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()

    # =====================================================
    # USER WAITING MESSAGE
    # =====================================================

    if language == "am":

        await message.answer(
            "⏳ <b>እባክዎ ትንሽ ይጠብቁ።</b>\n\n"

            "የክፍያ መረጃዎንና ደረሰኝዎን "
            "በትክክል ተልኮዋል።\n\n"

            "ማረጋገጫው ከተጠናቀቀ በኋላ "
            "የማረጋገጫ መልዕክት ይደርስዎታል።",
            parse_mode="HTML"
        )

    elif language == "or":

        await message.answer(
            "⏳ <b>Maaloo daqiiqaa tokko eegi.</b>\n\n"

            "Odeeffannoo kaffallii fi ragaan keessan milkaa’anii ergameera.\n\n"

            "Erga mirkaneeffame booda ergaa mirkaneessuu argattu.",
            parse_mode="HTML"
        )

    else:

        await message.answer(
            "⏳ <b>Please wait a moment.</b>\n\n"

            "Your payment information and receipt "
            "have been submitted successfully.\n\n"

            "You will receive a confirmation message "
            "after verification.",
            parse_mode="HTML"
        )

    # =====================================================
    # ADMIN MESSAGE
    # =====================================================

    admin_text = (

        "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"

        "🔔 <b>NEW PAYMENT SUBMISSION</b>\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        f"🆔 <b>Payment ID:</b> #{payment_id}\n\n"

        f"👤 <b>Name:</b>\n"
        f"{data['full_name']}\n\n"

        f"📱 <b>Phone:</b>\n"
        f"{data['phone']}\n\n"

        f"💳 <b>Payment Method:</b>\n"
        f"{payment_method.upper()}\n\n"

        f"🔢 <b>Transaction Reference:</b>\n"
        f"<code>{reference}</code>\n\n"

        f"👥 <b>Payment For:</b>\n"
        f"{data.get('payment_for', 'N/A')}\n\n"

        "⏳ <b>Status:</b> PENDING\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "⚠️ <b>ADMIN ACTION REQUIRED</b>\n\n"

        "Check the actual transaction in the "
        "authorized CBE/Telebirr system.\n\n"

        "Do NOT approve based only on the receipt.\n\n"

        f"Dashboard: {DASHBOARD_URL}"
    )

    # =====================================================
    # SEND TO ADMIN
    # =====================================================

    try:

        await bot.send_message(
            ADMIN_ID,
            admin_text,
            parse_mode="HTML",
            reply_markup=admin_payment_keyboard(
                payment_id
            )
        )

        # -------------------------------------------------
        # SEND RECEIPT
        # -------------------------------------------------

        if receipt_file_type == "photo":

            await bot.send_photo(
                ADMIN_ID,
                photo=receipt_file_id,
                caption=(
                    "🧾 <b>Payment Receipt</b>\n\n"
                    f"Payment ID: #{payment_id}"
                ),
                parse_mode="HTML"
            )

        else:

            await bot.send_document(
                ADMIN_ID,
                document=receipt_file_id,
                caption=(
                    "🧾 <b>Payment Receipt</b>\n\n"
                    f"Payment ID: #{payment_id}"
                ),
                parse_mode="HTML"
            )

    except Exception as exc:

        print(
            f"Failed to notify admin for payment #{payment_id}: {exc}"
        )

    # =====================================================
    # WAITING FOR ADMIN
    # =====================================================

    await state.set_state(
        RegistrationStates.waiting_for_admin
    )


# =========================================================
# MAIN
# =========================================================

async def main():

    print(
        "🚗 ETHIO CAR EQUB BOT IS RUNNING..."
    )
    print(f"Admin Telegram ID: {ADMIN_ID}")
    # Show configured admin dashboard URL (if set)
    try:
        print(f"Admin dashboard URL: {DASHBOARD_URL}")
    except Exception:
        pass

    await dp.start_polling(
        bot
    )


# =========================================================
# RUN
# =========================================================
# =========================================================
# ADMIN APPROVE PAYMENT
# =========================================================

# =========================================================
# MASK PHONE NUMBER
# =========================================================

def mask_phone(phone: str) -> str:

    phone = str(phone).strip()

    if len(phone) <= 6:
        return phone

    return phone[:4] + "****" + phone[-2:]


@dp.callback_query(
    F.data.startswith("approve_")
)
async def approve_payment(
    callback: CallbackQuery
):

    # -----------------------------------------------------
    # SECURITY CHECK
    # -----------------------------------------------------

    if callback.from_user.id != ADMIN_ID:

        await callback.answer(
            "❌ Unauthorized action.",
            show_alert=True
        )

        return

    # -----------------------------------------------------
    # GET PAYMENT ID
    # -----------------------------------------------------

    try:

        payment_id = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Invalid payment ID.",
            show_alert=True
        )

        return

    db = get_db()

    try:

        # -------------------------------------------------
        # FIND PAYMENT
        # -------------------------------------------------

        payment = db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

        # -------------------------------------------------
        # ENSURE PARTICIPANT SNAPSHOT
        # -------------------------------------------------
        # Fetch the user now so we can snapshot their name into the
        # payment record. This prevents later user profile changes from
        # altering the historical payment entry shown on the dashboard.
        user_for_snapshot = db.query(User).filter(
            User.id == payment.user_id
        ).first() if payment else None

        if not payment:

            await callback.answer(
                "❌ Payment not found.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # PREVENT DOUBLE APPROVAL
        # -------------------------------------------------

        if payment.status == "APPROVED":

            await callback.answer(
                "⚠️ This payment is already approved.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # PREVENT APPROVING REJECTED PAYMENT
        # -------------------------------------------------

        if payment.status == "REJECTED":

            await callback.answer(
                "⚠️ This payment was already rejected.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # APPROVE PAYMENT
        # -------------------------------------------------

        payment.status = "APPROVED"
        payment.verified_at = datetime.utcnow()

        # Snapshot participant name if not already set (covers older rows
        # created before migrations or cases where it was left NULL).
        if not payment.participant_name and user_for_snapshot:
            payment.participant_name = user_for_snapshot.participant_name

        # Snapshot participant phone if not already set so each payment keeps
        # the phone number the user had at approval time.
        if not getattr(payment, 'participant_phone', None) and user_for_snapshot:
            payment.participant_phone = user_for_snapshot.phone

        db.flush()

        approved_count = db.query(Payment).filter(
            Payment.status == "APPROVED"
        ).count()

        payment.participant_number = approved_count

        db.commit()

        # -------------------------------------------------
        # GET USER
        # -------------------------------------------------

        user = db.query(User).filter(
            User.id == payment.user_id
        ).first()

        if not user:

            await callback.answer(
                "⚠️ Payment approved, but user was not found.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # GENERATE PARTICIPANT NUMBER
        # -------------------------------------------------

        participant_number = payment.participant_number

        # -------------------------------------------------
        # USER CONFIRMATION
        # -------------------------------------------------

        if user.language == "or":
            confirmation_message = (
                "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"

                "🎉 <b>Hirmaannaa hirmaataa keessan mirkaneeffameera!</b>\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ Odeeffannoo kaffallii keessan adminiin mirkaneesseera.\n\n"

                f"🎟️ <b>Lakkofsa hirmaataa</b>\n"
                f"#{participant_number:03d}\n\n"

                f"👤 <b>Maqaa</b>\n"
                f"{user.participant_name}\n\n"

                f"📱 <b>Bilbila</b>\n"
                f"{mask_phone(user.phone)}\n\n"

                "💳 <b>Haala kaffallii</b>\n"
                "✅ Mirkaneeffame\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ ETHIO CAR EQUB keessatti keessatti galmaa’ameera.\n\n"

                "📢 Tarree hirmaattotaa Telegram channel keenya keessatti argama.\n\n"

                "🍀 <b>Carraa gaarii!</b>"
            )

        elif user.language == "am":
            confirmation_message = (
                "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"

                "🎉 <b>የተሳታፊ ምዝገባዎ ተረጋግጧል!</b>\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ የክፍያ መረጃዎ በአስተዳዳሪ "
                "ተረጋግጧል።\n\n"

                f"🎟️ <b>የተሳታፊ ቁጥር</b>\n"
                f"#{participant_number:03d}\n\n"

                f"👤 <b>ስም</b>\n"
                f"{user.participant_name}\n\n"

                f"📱 <b>ስልክ</b>\n"
                f"{mask_phone(user.phone)}\n\n"

                "💳 <b>የክፍያ ሁኔታ</b>\n"
                "✅ ተረጋግጧል\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ በETHIO CAR EQUB በትክክል "
                "ተመዝግበዋል።\n\n"

                "📢 የተሳታፊዎች ዝርዝር በTelegram "
                "ቻናላችን ላይ ይገኛል።\n\n"

                "🍀 <b>መልካም እድል!</b>"
            )

        else:
            confirmation_message = (
                "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"

                "🎉 <b>Your participant registration is confirmed!</b>\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ Your payment information has been verified by the admin.\n\n"

                f"🎟️ <b>Participant Number</b>\n"
                f"#{participant_number:03d}\n\n"

                f"👤 <b>Name</b>\n"
                f"{user.participant_name}\n\n"

                f"📱 <b>Phone</b>\n"
                f"{mask_phone(user.phone)}\n\n"

                "💳 <b>Payment Status</b>\n"
                "✅ Confirmed\n\n"

                "━━━━━━━━━━━━━━━━━━\n\n"

                "✅ You are successfully registered in ETHIO CAR EQUB.\n\n"

                "📢 The participant list is available in our Telegram channel.\n\n"

                "🍀 <b>Good luck!</b>"
            )

        # -------------------------------------------------
        # SEND USER CONFIRMATION
        # -------------------------------------------------

        bot = Bot(token=BOT_TOKEN)

        try:

            await bot.send_message(
                user.telegram_id,
                confirmation_message,
                parse_mode="HTML"
            )

        finally:

            await bot.session.close()

        # -------------------------------------------------
        # UPDATE ADMIN MESSAGE
        # -------------------------------------------------

        await callback.message.edit_reply_markup(
            reply_markup=None
        )

        await callback.message.answer(
            "✅ Payment approved successfully.\n"
            f"Participant number: #{participant_number:03d}"
        )

        await callback.answer(
            "✅ Payment approved.",
            show_alert=True
        )

    except Exception as e:

        db.rollback()

        print(
            f"APPROVE ERROR: {e}"
        )

        await callback.answer(
            "❌ An error occurred while approving.",
            show_alert=True
        )

    finally:

        db.close()


# =========================================================
# ADMIN REJECT PAYMENT
# =========================================================

@dp.callback_query(
    F.data.startswith("reject_")
)
async def reject_payment(
    callback: CallbackQuery
):

    # -----------------------------------------------------
    # SECURITY CHECK
    # -----------------------------------------------------

    if callback.from_user.id != ADMIN_ID:

        await callback.answer(
            "❌ Unauthorized action.",
            show_alert=True
        )

        return

    # -----------------------------------------------------
    # GET PAYMENT ID
    # -----------------------------------------------------

    try:

        payment_id = int(
            callback.data.split("_")[1]
        )

    except (ValueError, IndexError):

        await callback.answer(
            "❌ Invalid payment ID.",
            show_alert=True
        )

        return

    db = get_db()

    try:

        # -------------------------------------------------
        # FIND PAYMENT
        # -------------------------------------------------

        payment = db.query(Payment).filter(
            Payment.id == payment_id
        ).first()

        if not payment:

            await callback.answer(
                "❌ Payment not found.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # PREVENT DOUBLE REJECTION
        # -------------------------------------------------

        if payment.status == "REJECTED":

            await callback.answer(
                "⚠️ This payment is already rejected.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # PREVENT REJECTING APPROVED PAYMENT
        # -------------------------------------------------

        if payment.status == "APPROVED":

            await callback.answer(
                "⚠️ This payment is already approved.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # REJECT PAYMENT
        # -------------------------------------------------

        payment.status = "REJECTED"
        payment.verified_at = datetime.utcnow()

        payment.rejection_reason = (
            "Payment was rejected by administrator."
        )

        db.commit()

        # -------------------------------------------------
        # GET USER
        # -------------------------------------------------

        user = db.query(User).filter(
            User.id == payment.user_id
        ).first()

        if not user:

            await callback.answer(
                "⚠️ Payment rejected, but user was not found.",
                show_alert=True
            )

            return

        # -------------------------------------------------
        # USER REJECTION MESSAGE
        # -------------------------------------------------

        rejection_message = (
            "🚗✨ <b>ETHIO CAR EQUB</b> ✨🚗\n\n"

            "❌ <b>የክፍያ ማረጋገጫ አልተሳካም</b>\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "ያስገቡት የክፍያ መረጃ "
            "በአስተዳዳሪ ማረጋገጫ አልፏል።\n\n"

            "እባክዎ የክፍያዎን ደረሰኝ እና "
            "የግብይት ቁጥር በትክክል ያረጋግጡ።\n\n"

            "🔄 ከዚያ እንደገና ይላኩ።\n\n"

            "━━━━━━━━━━━━━━━━━━\n\n"

            "🙏 እናመሰግናለን።"
        )

        # -------------------------------------------------
        # SEND REJECTION TO USER
        # -------------------------------------------------

        bot = Bot(token=BOT_TOKEN)

        try:

            await bot.send_message(
                user.telegram_id,
                rejection_message,
                parse_mode="HTML"
            )

        finally:

            await bot.session.close()

        # -------------------------------------------------
        # UPDATE ADMIN MESSAGE
        # -------------------------------------------------

        await callback.message.edit_reply_markup(
            reply_markup=None
        )

        await callback.message.answer(
            "❌ Payment rejected."
        )

        await callback.answer(
            "❌ Payment rejected.",
            show_alert=True
        )

    except Exception as e:

        db.rollback()

        print(
            f"REJECT ERROR: {e}"
        )

        await callback.answer(
            "❌ An error occurred while rejecting.",
            show_alert=True
        )

    finally:

        db.close()
        
        
if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print(
            "🛑 ETHIO CAR EQUB BOT STOPPED."
        )
        