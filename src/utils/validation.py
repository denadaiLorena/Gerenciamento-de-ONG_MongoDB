import re
from datetime import datetime

DIGITS_RE = re.compile(r"\D+")


def strip_non_digits(s: str) -> str:
    if s is None:
        return ""
    return re.sub(DIGITS_RE, "", s)


# Masks formatting (not live typing), apply formatting to a raw numeric string
def format_cpf(value: str) -> str:
    v = strip_non_digits(value)
    if len(v) != 11:
        return value
    return f"{v[0:3]}.{v[3:6]}.{v[6:9]}-{v[9:11]}"


def format_cnpj(value: str) -> str:
    v = strip_non_digits(value)
    if len(v) != 14:
        return value
    return f"{v[0:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"


def format_date(value: str) -> str:
    # expect DDMMYYYY or DD/MM/YYYY
    v = strip_non_digits(value)
    if len(v) != 8:
        return value
    return f"{v[0:2]}/{v[2:4]}/{v[4:8]}"


def format_phone(value: str) -> str:
    v = strip_non_digits(value)
    if len(v) == 10:
        return f"({v[0:2]}) {v[2:6]}-{v[6:10]}"
    if len(v) == 11:
        return f"({v[0:2]}) {v[2:7]}-{v[7:11]}"
    return value


def format_cep(value: str) -> str:
    v = strip_non_digits(value)
    if len(v) != 8:
        return value
    return f"{v[0:5]}-{v[5:8]}"


# Validators

def is_valid_cpf(cpf: str) -> bool:
    """Valida CPF com dígitos verificadores."""
    v = strip_non_digits(cpf)
    if len(v) != 11:
        return False
    # rejeita sequências repetidas
    if v == v[0] * 11:
        return False

    def calc(digs):
        s = sum(int(d) * w for d, w in zip(digs, range(len(digs) + 1, 1, -1)))
        r = (s * 10) % 11
        return r if r < 10 else 0

    first = calc(v[:9])
    second = calc(v[:10])
    return first == int(v[9]) and second == int(v[10])


def is_valid_cnpj(cnpj: str) -> bool:
    v = strip_non_digits(cnpj)
    if len(v) != 14:
        return False
    if v == v[0] * 14:
        return False

    def calc(digs, multipliers):
        s = sum(int(d) * m for d, m in zip(digs, multipliers))
        r = s % 11
        return 0 if r < 2 else 11 - r

    mult1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    mult2 = [6] + mult1
    first = calc(v[:12], mult1)
    second = calc(v[:13], mult2)
    return first == int(v[12]) and second == int(v[13])


def is_valid_date(date_str: str, allow_future: bool = False) -> bool:
    try:
        # Accepts DD/MM/YYYY or plain digits
        s = date_str.strip()
        if "/" in s:
            dt = datetime.strptime(s, "%d/%m/%Y")
        else:
            v = strip_non_digits(s)
            if len(v) != 8:
                return False
            dt = datetime.strptime(f"{v[0:2]}/{v[2:4]}/{v[4:8]}", "%d/%m/%Y")
        if not allow_future and dt.date() > datetime.now().date():
            return False
        return True
    except Exception:
        return False


def is_valid_phone(phone: str) -> bool:
    v = strip_non_digits(phone)
    return len(v) in (10, 11)


def is_valid_cep(cep: str) -> bool:
    v = strip_non_digits(cep)
    return len(v) == 8


def require_field(value: str, field_name: str) -> tuple[bool, str]:
    if value is None or str(value).strip() == "":
        return False, f"Preencha o campo obrigatório: {field_name}"
    return True, ""


def normalize_numeric_field(value: str) -> str:
    return strip_non_digits(value)
