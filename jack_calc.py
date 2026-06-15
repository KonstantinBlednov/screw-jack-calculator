import streamlit as st
import math

# Настройка страницы
st.set_page_config(page_title="Расчет домкрата / пресса", layout="wide")

# --- СЛОВАРЬ ЛОКАЛИЗАЦИИ (LOCALIZATION DICTIONARY) ---
LANG_DICT = {
    "title": {"EN": "Screw Jack / Press Calculator", "RU": "Расчет домкрата / пресса"},
    "subtitle": {"EN": "Thread parameters in the range of 6 to 100 mm", "RU": "Параметры резьбы в диапазоне от 6 до 100 мм"},
    "lang_sel": {"EN": "Interface Language", "RU": "Язык интерфейса"},
    
    # Секция 1
    "h_drive": {"EN": "1. Drive Parameters (Lever)", "RU": "1. Параметры привода (Рычаг)"},
    "f_handle": {"EN": "Force on lever F_handle, (N)", "RU": "Сила на рычаге F_руч, (Н)"},
    "r_lever": {"EN": "Lever arm length R, (mm)", "RU": "Длина плеча рычага R, (мм)"},
    
    # Секция 2
    "h_thread": {"EN": "2. Thread Type & Parameters", "RU": "2. Выбор типа и параметров резьбы"},
    "t_type": {"EN": "Thread profile type", "RU": "Тип профиля резьбы"},
    "t_trap": {"EN": "Trapezoidal (GOST 9484)", "RU": "Трапецеидальная (ГОСТ 9484)"},
    "t_butt": {"EN": "Buttress (GOST 10177)", "RU": "Упорная (ГОСТ 10177)"},
    "t_metr": {"EN": "Metric (GOST 24705)", "RU": "Метрическая (ГОСТ 24705)"},
    "d_nom": {"EN": "Nominal outer diameter d, (mm)", "RU": "Номинальный наружный диаметр d, (мм)"},
    "p_pitch": {"EN": "Thread pitch P, (mm)", "RU": "Шаг резьбы P, (мм)"},
    "l_stroke": {"EN": "Working stroke L, (mm)", "RU": "Рабочий ход винта L, (мм)"},
    
    # Секция 3
    "h_bearing": {"EN": "3. Screw End Support (Thrust Collar)", "RU": "3. Опорный торец винта (Пята)"},
    "b_type": {"EN": "Thrust collar friction type", "RU": "Вид трения торца винта"},
    "b_ball": {"EN": "Thrust ball bearing (rolling friction)", "RU": "Упорный шарикоподшипник (качения)"},
    "b_lub": {"EN": "Lubricated sliding (steel on steel/bronze)", "RU": "Скольжение со смазкой (сталь по стали/бронзе)"},
    "b_dry": {"EN": "Unlubricated sliding (dry friction)", "RU": "Скольжение без смазки (сухое трение)"},
    "d_sr_t": {"EN": "Mean bearing diameter D_mean_t, (mm)", "RU": "Средний диаметр опоры торца D_ср_т, (мм)"},
    "d_sr_t_help": {"EN": "Mean diameter of the collar friction surface. Default is nominal diameter d.", "RU": "Средний диаметр поверхности трения торца. По умолчанию равен номинальному диаметру винта d."},
    
    # Секция 4
    "h_mat": {"EN": "4. Materials & Construction", "RU": "4. Материалы и Конструкция"},
    "m_screw": {"EN": "Screw material", "RU": "Материал винта"},
    "scr_hard": {"EN": "Steel 45 (Hardened)", "RU": "Сталь 45 (Закалка)"},
    "scr_norm": {"EN": "Steel 45 (Normalized)", "RU": "Сталь 45 (Нормализация)"},
    "scr_st3": {"EN": "Steel 3 / St3", "RU": "Сталь 3 / Ст3"},
    "cap_scr_hard": {"EN": "💡 *High strength, surface hardness. Reduces thread wear and galling risks.*", "RU": "💡 *Высокая прочность, твердость поверхности. Снижает износ резьбы и риск задиров.*"},
    "cap_scr_norm": {"EN": "💡 *Good machinability, medium strength. Classic choice for low-stress screws.*", "RU": "💡 *Хорошая обрабатываемость, средняя прочность. Классический выбор для ненапряженных винтов.*"},
    "cap_scr_st3": {"EN": "💡 *Low strength. Used only for light, low-capacity manual jacks.*", "RU": "💡 *Низкая прочность. Применяется только для легких ручных домкратов малой грузоподъемности.*"},
    
    "m_nut": {"EN": "Nut material", "RU": "Материал гайки"},
    "nut_br1": {"EN": "Bronze BrO10F1", "RU": "Бронза БрО10Ф1"},
    "nut_br2": {"EN": "Bronze BrA9Zh3", "RU": "Бронза БрА9Ж3"},
    "nut_iron": {"EN": "Antifriction Cast Iron", "RU": "Антифрикционный чугун"},
    "nut_steel": {"EN": "Steel (St5, Steel 45)", "RU": "Сталь (Ст5, Сталь 45)"},
    "cap_nut_br1": {"EN": "💡 *Ideal antifriction pair (f=0.08). High allowable pressure, excellent run-in.*", "RU": "💡 *Идеальная антифрикционная пара (f=0.08). Высокое допускаемое давление, отличная прирабатываемость.*"},
    "cap_nut_br2": {"EN": "💡 *High crush strength. Slightly higher friction (f=0.10). Requires good lubrication.*", "RU": "💡 *Высокая прочность на смятие. Трение чуть выше (f=0.10). Требует хорошей смазки и приработки.*"},
    "cap_nut_iron": {"EN": "💡 *Cost-effective for low speeds. Risk of brittle thread shearing under impact (f=0.12).*", "RU": "💡 *Бюджетный вариант для малых скоростей. Склонность к хрупкому скалыванию витков при ударах (f=0.12).*"},
    "cap_nut_st_hard": {"EN": "💡 *Highly loaded pair (f=0.12). Requires continuous lubrication to prevent seizing.*", "RU": "💡 *Тяжелонагруженная пара (f=0.12). Требует обильной непрерывной смазки во избежание заклинивания.*"},
    "cap_nut_st_raw": {"EN": "⚠️ *Dangerous unhardened Steel/Steel pair (f=0.15). Prone to galling, seizing, and rapid wear!*", "RU": "⚠️ *Опасная сырая пара Сталь/Сталь (f=0.15). Склонна к задирам, схватыванию и быстрому износу резьбы!*"},
    
    "psi_h": {"EN": "Nut height coefficient (ψ_H)", "RU": "Коэффициент высоты гайки (ψ_H)"},
    "h_fix": {"EN": "Screw support constraints", "RU": "Опоры винта (схема закрепления)"},
    "fix_1": {"EN": "1. Fixed-Free [mu = 2.0]", "RU": "1. Один конец защемлен, второй свободен [mu = 2.0]"},
    "fix_2": {"EN": "2. Pinned-Pinned [mu = 1.0]", "RU": "2. Оба конца шарнирные [mu = 1.0]"},
    "fix_3": {"EN": "3. Fixed-Pinned [mu = 0.7]", "RU": "3. Один конец защемлен, второй шарнирный [mu = 0.7]"},
    "fix_4": {"EN": "4. Fixed-Fixed [mu = 0.5]", "RU": "4. Оба конца защемлены [mu = 0.5]"},
    "cap_fix_1": {"EN": "⚠️ *Low stability. Screw is rigidly clamped at base, working end is free. Design length doubles.*", "RU": "⚠️ *Низкая устойчивость. Винт жестко зажат в основании, рабочий торец свободен. Длина винта для расчета удваивается.*"},
    "cap_fix_2": {"EN": "💡 *Standard layout. Screw is centered at both ends (e.g., lower support + slider in rigid guides).*", "RU": "💡 *Стандартная схема. Винт центрируется с обоих концов (например, нижняя опора + ползун в жестких направляющих).*"},
    "cap_fix_3": {"EN": "💡 *Increased stiffness. Base rigidly restrains tilting, nut/working end is guided.*", "RU": "💡 *Повышенная жесткость. Базовая опора жестко держит винт от перекоса (два подшипника), а гайка/торец имеет надежное направление.*"},
    "cap_fix_4": {"EN": "⚡ *Maximum rigidity. Screw is strictly constrained against angular misalignment at both ends.*", "RU": "⚡ *Максимальная жесткость и устойчивость. Винт жестко зафиксирован от перекосов в подшипниковых узлах с обоих концов.*"},

    # Результаты вывода
    "res_header": {"EN": "Results for standard thread:", "RU": "Результаты для стандартной резьбы:"},
    "m_force": {"EN": "Developed Axial Force F", "RU": "Развиваемое осевое усилие F"},
    "m_capacity": {"EN": "Useful Load Capacity", "RU": "Полезная грузоподъемность"},
    "m_eff": {"EN": "Total Mechanism Efficiency (η_total)", "RU": "Общий КПД механизма (η_общ)"},
    "dist_torque": {"EN": "Torque Distribution", "RU": "Распределение крутящего момента"},
    "text_f": {"EN": "Thread friction", "RU": "Трение в резьбе"},
    "text_by_nut": {"EN": "by nut material", "RU": "по материалу гайки"},
    "text_f_p": {"EN": "Bearing collar friction", "RU": "Трение на опорном торце винта"},
    "m_rezb": {"EN": "Thread Torque", "RU": "Момент на резьбе"},
    "m_torec": {"EN": "Collar Friction Torque", "RU": "Момент трения на торце (пяте)"},
    "m_total_nm": {"EN": "Total Lever Torque", "RU": "Полный момент рычага"},
    
    # Колонки проверок
    "col_screw": {"EN": "Screw Rod Check", "RU": "Проверка стержня винта"},
    "d3_text": {"EN": "Minor thread diameter d₃:", "RU": "Внутренний диаметр резьбы d₃:"},
    "sigma_text": {"EN": "Equivalent stress:", "RU": "Эквивалентное напряжение:"},
    "p_ok": {"EN": "✅ Strength ensured", "RU": "✅ Прочность обеспечена"},
    "p_fail": {"EN": "❌ MATERIAL WILL FAIL!", "RU": "❌ МАТЕРИАЛ НЕ ВЫДЕРЖИТ!"},
    "buck_fail": {"EN": "❌ Buckling risk! Safety factor:", "RU": "❌ Риск продольного изгиба! Запас:"},
    "buck_ok": {"EN": "✅ No buckling danger", "RU": "✅ Опасности продольного изгиба нет"},
    
    "col_nut": {"EN": "Nut Check", "RU": "Проверка гайки"},
    "h_nut_text": {"EN": "Nut height:", "RU": "Высота гайки:"},
    "threads_text": {"EN": "threads", "RU": "витков"},
    "q_text": {"EN": "Thread pressure q", "RU": "Давление в резьбе q"},
    "q_adm_text": {"EN": "Allowable:", "RU": "Допускаемое:"},
    "q_ok": {"EN": "✅ Nut threads will withstand the load", "RU": "✅ Витки гайки выдержат нагрузку"},
    "q_fail": {"EN": "❌ Threads will crush!", "RU": "❌ Резьба сомнется!"},
    
    "col_self": {"EN": "Self-Locking Conditions", "RU": "Условия самоторможения"},
    "self_ok": {"EN": "✅ Self-locking ensured", "RU": "✅ Самоторможение обеспечено"},
    "self_fail": {"EN": "❌ NO Self-locking!", "RU": "❌ Самоторможения НЕТ!"}
}

# --- ВЫБОР ЯЗЫКА В БОКОВОЙ ПАНЕЛИ ---
st.sidebar.markdown("### 🌐 Localization / Локализация")
lang = st.sidebar.radio(LANG_DICT["lang_sel"]["EN"], ["EN", "RU"], index=0)

# Функция перевода
def _(key):
    return LANG_DICT[key].get(lang, LANG_DICT[key]["EN"])

# Заголовки страницы
st.title(_("title"))
st.write(_("subtitle"))
st.markdown("---")

# --- БАЗА ДАННЫХ СТАНДАРТНЫХ РЕЗЬБ (ГОСТ) ---
TR_UP_THREADS = {
    6: [1, 1.5], 7: [1, 1.5], 8: [1.5, 2], 10: [1.5, 2, 3], 12: [2, 3], 14: [2, 3],
    16: [2, 3, 4], 18: [2, 4], 20: [2, 3, 4, 6], 22: [3, 5, 8], 24: [3, 5, 8],
    26: [3, 5, 8], 28: [3, 5, 8], 30: [3, 6, 10], 32: [3, 6, 10], 34: [3, 6, 10],
    36: [3, 6, 10], 40: [3, 7, 12], 44: [3, 7, 12], 48: [3, 8, 12], 50: [3, 8, 12],
    52: [3, 8, 12], 55: [3, 9, 14], 60: [3, 9, 14], 65: [4, 10, 16], 70: [4, 10, 16],
    75: [4, 10, 16], 80: [4, 10, 16], 85: [4, 12, 18], 90: [4, 12, 18], 95: [4, 12, 18],
    100: [4, 12, 20]
}

METRIC_THREADS = {
    6: [0.5, 0.75, 1.0], 8: [0.5, 0.75, 1.0, 1.25], 10: [0.75, 1.0, 1.25, 1.5],
    12: [1.0, 1.25, 1.5, 1.75], 14: [1.0, 1.25, 1.5, 2.0], 16: [1.0, 1.5, 2.0],
    18: [1.0, 1.5, 2.0, 2.5], 20: [1.0, 1.5, 2.0, 2.5], 22: [1.0, 1.5, 2.0, 2.5],
    24: [1.0, 1.5, 2.0, 3.0], 27: [1.0, 1.5, 2.0, 3.0], 30: [1.0, 1.5, 2.0, 3.5],
    33: [1.5, 2.0, 3.5], 36: [1.5, 2.0, 3.0, 4.0], 39: [1.5, 2.0, 3.0, 4.0],
    42: [1.5, 2.0, 3.0, 4.5], 45: [1.5, 2.0, 3.0, 4.5], 48: [1.5, 2.0, 3.0, 4.0, 5.0],
    52: [1.5, 2.0, 3.0, 4.0, 5.0], 56: [2.0, 3.0, 4.0, 5.5], 60: [2.0, 3.0, 4.0, 5.5],
    64: [2.0, 3.0, 4.0, 6.0], 68: [2.0, 3.0, 4.0, 6.0], 72: [2.0, 3.0, 4.0, 6.0],
    76: [2.0, 3.0, 4.0, 6.0], 80: [2.0, 3.0, 4.0, 6.0], 85: [2.0, 3.0, 4.0, 6.0],
    90: [2.0, 3.0, 4.0, 6.0], 95: [2.0, 3.0, 4.0, 6.0], 100: [2.0, 3.0, 4.0, 6.0]
}

# --- ЛЕВАЯ ПАНЕЛЬ: ВХОДНЫЕ ДАННЫЕ ---
st.sidebar.header(_("h_drive"))
F_handle = st.sidebar.number_input(_("f_handle"), value=150, step=10)
R_lever = st.sidebar.number_input(_("r_lever"), value=400, step=50)

st.sidebar.header(_("h_thread"))
t_options = [_("t_trap"), _("t_butt"), _("t_metr")]
thread_type_sel = st.sidebar.selectbox(_("t_type"), t_options)

if thread_type_sel == _("t_metr"):
    available_diameters = sorted(list(METRIC_THREADS.keys()))
    db = METRIC_THREADS
else:
    available_diameters = sorted(list(TR_UP_THREADS.keys()))
    db = TR_UP_THREADS

default_d_index = available_diameters.index(32) if 32 in available_diameters else 0
d = st.sidebar.selectbox(_("d_nom"), available_diameters, index=default_d_index)

available_pitches = db[d]
default_p_index = available_pitches.index(6) if 6 in available_pitches else 0
P = st.sidebar.selectbox(_("p_pitch"), available_pitches, index=default_p_index)

L = st.sidebar.number_input(_("l_stroke"), value=300, step=10)

st.sidebar.header(_("h_bearing"))
b_options = [_("b_ball"), _("b_lub"), _("b_dry")]
bearing_type = st.sidebar.selectbox(_("b_type"), b_options)

if bearing_type == _("b_ball"):
    f_p = 0.01
elif bearing_type == _("b_lub"):
    f_p = 0.11
else:
    f_p = 0.18

D_sr_t = st.sidebar.number_input(_("d_sr_t"), value=float(d), step=1.0, help=_("d_sr_t_help"))

st.sidebar.header(_("h_mat"))
scr_options = [_("scr_hard"), _("scr_norm"), _("scr_st3")]
material_screw = st.sidebar.selectbox(_("m_screw"), scr_options)

if material_screw == _("scr_hard"):
    st.sidebar.caption(_("cap_scr_hard"))
    sigma_adm = 120.0
elif material_screw == _("scr_norm"):
    st.sidebar.caption(_("cap_scr_norm"))
    sigma_adm = 90.0
else:
    st.sidebar.caption(_("cap_scr_st3"))
    sigma_adm = 60.0

st.sidebar.markdown(" ")

nut_options = [_("nut_br1"), _("nut_br2"), _("nut_iron"), _("nut_steel")]
material_nut = st.sidebar.selectbox(_("m_nut"), nut_options)

if material_nut == _("nut_br1"):
    st.sidebar.caption(_("cap_nut_br1"))
    q_adm = 12.0
    f_friction = 0.08
elif material_nut == _("nut_br2"):
    st.sidebar.caption(_("cap_nut_br2"))
    q_adm = 10.0
    f_friction = 0.10
elif material_nut == _("nut_iron"):
    st.sidebar.caption(_("cap_nut_iron"))
    q_adm = 5.0
    f_friction = 0.12
else:
    if material_screw == _("scr_hard"):
        st.sidebar.caption(_("cap_nut_st_hard"))
        f_friction = 0.12
    else:
        st.sidebar.caption(_("cap_nut_st_raw"))
        f_friction = 0.15
    q_adm = 7.5

st.sidebar.markdown(" ")
psi_H = st.sidebar.slider(_("psi_h"), 1.2, 2.5, 1.8, step=0.1)

fix_options = [_("fix_1"), _("fix_2"), _("fix_3"), _("fix_4")]
fix_type = st.sidebar.selectbox(_("h_fix"), fix_options)

if fix_type == _("fix_1"):
    st.sidebar.caption(_("cap_fix_1"))
    mu = 2.0
elif fix_type == _("fix_2"):
    st.sidebar.caption(_("cap_fix_2"))
    mu = 1.0
elif fix_type == _("fix_3"):
    st.sidebar.caption(_("cap_fix_3"))
    mu = 0.7
else:
    st.sidebar.caption(_("cap_fix_4"))
    mu = 0.5


# --- МАТЕМАТИЧЕСКИЙ РАСЧЕТ ---
M_total = F_handle * R_lever
M_total_nm = M_total / 1000

if thread_type_sel == _("t_trap"):
    gamma_deg = 15.0
    h = 0.5 * P
    d2 = d - 0.5 * P
    d3 = d - P
elif thread_type_sel == _("t_butt"):
    gamma_deg = 3.0
    h = 0.5 * P
    d2 = d - 0.75 * P
    d3 = d - 1.5 * P
else:
    gamma_deg = 30.0
    h = 0.54125 * P
    d2 = d - 0.6495 * P
    d3 = d - 1.2268 * P

tan_psi = P / (math.pi * d2)
psi_rad = math.atan(tan_psi)
psi_deg = math.degrees(psi_rad)

alpha_half = math.radians(gamma_deg)
tan_phi_prime = f_friction / math.cos(alpha_half)
phi_prime_rad = math.atan(tan_phi_prime)
phi_prime_deg = math.degrees(phi_prime_rad)

denominator = (d2 / 2) * math.tan(psi_rad + phi_prime_rad) + f_p * (D_sr_t / 2)
F = M_total / denominator
F_kn = F / 1000

M_rezb = F * (d2 / 2) * math.tan(psi_rad + phi_prime_rad)
M_torec = F * f_p * (D_sr_t / 2)
eff_total = (F * P) / (2 * math.pi * M_total) * 100 if M_total > 0 else 0

A3 = (math.pi * (d3**2)) / 4
sigma_szh = F / A3 if A3 > 0 else 0
Wp = math.pi * d3**3 / 16
tau_k = M_rezb / Wp if Wp > 0 else 0
sigma_ekv = math.sqrt(sigma_szh**2 + 3 * tau_k**2)

H_nut = psi_H * d2
z_vitkov = max(1, math.floor(H_nut / P))

if thread_type_sel == _("t_trap"):
    h_work = 0.5 * P + 0.25
elif thread_type_sel == _("t_butt"):
    h_work = 0.75 * P
else:
    h_work = 0.5413 * P

A_contact = math.pi * d2 * h_work * z_vitkov
q_calc = F / A_contact if A_contact > 0 else 0

L_priv = mu * L
E_modul = 2.0e5
I = math.pi * d3**4 / 64
F_cr = (math.pi**2 * E_modul * I) / (L_priv**2)
k_ust = F_cr / F if F > 0 else float("inf")


# --- ВЫВОД РЕЗУЛЬТАТОВ ---
profile_short = "Metric" if thread_type_sel == _("t_metr") else ("Trapezoidal" if thread_type_sel == _("t_trap") else "Buttress")
st.subheader(f"{_('res_header')} {profile_short} {d}х{P}")

c_res1, c_res2, c_res3 = st.columns(3)
c_res1.metric(_("m_force"), f"{F_kn:.2f} kN" if lang == "EN" else f"{F_kn:.2f} кН")
c_res2.metric(_("m_capacity"), f"~ {F/9.81:.0f} kg" if lang == "EN" else f"~ {F/9.81:.0f} кг")
c_res3.metric(_("m_eff"), f"{eff_total:.1f} %")

st.markdown("---")
st.subheader(_("dist_torque"))

scr_short = "Steel 45" if "45" in material_screw else "Steel 3"
st.write(f"{_('text_f')} ({scr_short} {_('text_by_nut')}) $f$ = **{f_friction}** | {_('text_f_p')} $f_п$ = **{f_p}**")

cm1, cm2, cm3 = st.columns(3)
cm1.metric(_("m_rezb"), f"{M_rezb/1000:.1f} N·m" if lang == "EN" else f"{M_rezb/1000:.1f} Н·м")
cm2.metric(_("m_torec"), f"{M_torec/1000:.1f} N·m" if lang == "EN" else f"{M_torec/1000:.1f} Н·м")
cm3.metric(_("m_total_nm"), f"{M_total_nm:.1f} N·m" if lang == "EN" else f"{M_total_nm:.1f} Н·м")

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.header(_("col_screw"))
    st.write(f"{_('d3_text')} **{d3:.2f} mm**" if lang == "EN" else f"{_('d3_text')} **{d3:.2f} мм**")
    st.write(f"{_('sigma_text')} **{sigma_ekv:.1f} MPa**" if lang == "EN" else f"{_('sigma_text')} **{sigma_ekv:.1f} МПа**")
    
    if sigma_ekv <= sigma_adm:
        st.success(f"{_('p_ok')} (≤ {sigma_adm} {'MPa' if lang == 'EN' else 'МПа'})")
    else:
        st.error(_("p_fail"))
        
    if k_ust < 3.0:
        st.error(f"{_('buck_fail')} {k_ust:.2f}")
    else:
        st.success(_("buck_ok"))

with col2:
    st.header(_("col_nut"))
    st.write(f"{_('h_nut_text')} **{H_nut:.1f} mm** ({z_vitkov} {_('threads_text')})" if lang == "EN" else f"{_('h_nut_text')} **{H_nut:.1f} мм** ({z_vitkov} {_('threads_text')})")
    
    st.metric(_("q_text"), f"{q_calc:.1f} MPa" if lang == "EN" else f"{q_calc:.1f} МПа", 
              delta=f"{_('q_adm_text')} {q_adm} {'MPa' if lang == 'EN' else 'МПа'}")
    
    if q_calc <= q_adm:
        st.success(_("q_ok"))
    else:
        st.error(_("q_fail"))

with col3:
    st.header(_("col_self"))
    if psi_deg < phi_prime_deg:
        st.success(f"{_('self_ok')} (ψ = {psi_deg:.1f}° < φ' = {phi_prime_deg:.1f}°)")
    else:
        st.error(f"{_('self_fail')} (ψ = {psi_deg:.1f}°)")