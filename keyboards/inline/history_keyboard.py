from telebot.util import quick_markup


def history_periods_keyboard():
    '''Создание inline клавиатуры для вариантов периодов отображения истории (а также отмены либо удаления
    истории поиска.'''
    return quick_markup(
            {
                'За день': {'callback_data': 'hist_day'},
                'За неделю': {'callback_data': 'hist_week'},
                'За месяц': {'callback_data': 'hist_month'},
                'Удаление истории поиска': {'callback_data': 'hist_delete'},
                'Отмена операции': {'callback_data': 'hist_cancel'}
            }, row_width=3
        )
