def get_key(d, value):
    """Функция возвращает из словаря значение по ключу."""
    for k, v in d.items():
        if v == value:
            print(k)
            return k
