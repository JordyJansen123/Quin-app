# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 13:25:55 2025

@author: jordy
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Quinn — FinTech Assistant",
    page_icon="💬",
    layout="wide",
)

# =========================================================
# BRAND COLORS (zoals gevraagd)
# =========================================================
PRIMARY = "#000000"      # wit
SECONDARY1 = "#C3EAFF"   # lichtblauw
SECONDARY2 = "#EDEDED"   # lichtgrijs
BG_DARK = "#0F1116"
BG_DARK_LIGHT = "#181B20"
BORDER = "#2A2E33"

# =========================================================
# CUSTOM CSS — FinTech look & feel
# =========================================================
CSS = f"""
<style>
body {{
    background-color: {BG_DARK};
}}

.main {{
    background-color: {BG_DARK};
}}

section[data-testid="stSidebar"] {{
    background-color: {BG_DARK_LIGHT};
    border-right: 1px solid {BORDER};
}}

h1, h2, h3, h4, h5, h6, p, label {{
    color: {PRIMARY};
}}

.chat-container {{
    height: 520px;
    overflow-y: auto;
    padding: 20px;
    background-color: {BG_DARK_LIGHT};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}

.chat-bubble-user {{
    background-color: {SECONDARY1};
    color: #000000;
    padding: 12px 15px;
    border-radius: 16px;
    max-width: 70%;
    margin-left: auto;
    margin-bottom: 8px;
    font-size: 15px;
    border: 1px solid {SECONDARY2};
}}

.chat-bubble-bot {{
    background-color: {SECONDARY2};
    color: #000000;
    padding: 12px 15px;
    border-radius: 16px;
    border: 1px solid {SECONDARY1};
    max-width: 70%;
    margin-right: auto;
    margin-bottom: 8px;
    font-size: 15px;
}}

.timestamp {{
    font-size: 11px;
    opacity: 0.6;
    margin-top: 3px;
    text-align: right;
}}

.quick-btn {{
    background-color: {BG_DARK_LIGHT};
    border-radius: 999px;
    padding: 6px 12px;
    border: 1px solid {SECONDARY2};
    color: {PRIMARY};
    font-size: 13px;
    cursor: pointer;
}}

.quick-btn:hover {{
    border-color: {SECONDARY1};
}}

.disclaimer {{
    font-size: 11px;
    color: {SECONDARY2};
    opacity: 0.75;
}}

.metric-label {{
    color: {SECONDARY2};
    font-size: 13px;
}}

.stTextInput>div>div>input {{
    background-color: {BG_DARK_LIGHT};
    border: 1px solid {SECONDARY2};
    color: {PRIMARY};
}}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "risk_profile" not in st.session_state:
    st.session_state["risk_profile"] = "Neutraal"


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def detect_intent(text: str) -> str:
    """Zeer eenvoudige intent-herkenning op basis van keywords."""
    t = text.lower()
    if any(k in t for k in ["aandeel", "stock", "equity", "etf"]):
        return "equities"
    if any(k in t for k in ["crypto", "bitcoin", "btc", "eth", "ethereum"]):
        return "crypto"
    if any(k in t for k in ["rente", "interest", "hypotheek", "lening", "loan"]):
        return "rates"
    if any(k in t for k in ["portefeuille", "portfolio", "allocatie", "allocation"]):
        return "portfolio"
    if any(k in t for k in ["risico", "volatiliteit", "drawdown"]):
        return "risk"
    if any(k in t for k in ["inflatie", "inflation", "cpi"]):
        return "inflation"
    if any(k in t for k in ["advies", "advies nodig", "wat moet ik doen"]):
        return "advice"
    return "general"


def quinn_reply(text: str, risk_profile: str) -> str:
    """Generieke Quinn-respons op basis van intent + risicoprofiel."""
    intent = detect_intent(text)
    t = text.lower()

    # Greetings
    if any(g in t for g in ["hallo", "hoi", "hey", "hi", "goedemorgen", "goedemiddag"]):
        return (
            f"Hoi! Ik ben Quinn, jouw FinTech-assistant. "
            f"Je huidige risicoprofiel staat op **{risk_profile}**. "
            "Waar wil je het over hebben: aandelen, crypto, rente, portefeuille of iets anders?"
        )

    # Intent-specifieke antwoorden
    if intent == "equities":
        base = (
            "Aandelen (equities) bewegen op basis van winstgroei, waardering en marktsentiment. "
        )
        if risk_profile == "Defensief":
            return (
                base
                + "Met een defensief profiel liggen brede index-ETF’s en sectoren als "
                "gezondheidszorg en consumentenbasis vaak meer in lijn met je risicotolerantie."
            )
        if risk_profile == "Offensief":
            return (
                base
                + "Met een offensief profiel wordt vaak gekeken naar groeiaandelen, "
                "opkomende markten en sectoren als technologie. Diversificatie blijft belangrijk."
            )
        return (
            base
            + "Met een neutraal profiel wordt vaak gekozen voor een mix tussen stabiele large caps "
            "en wat groeigerichte posities."
        )

    if intent == "crypto":
        return (
            "Crypto is een zeer volatiele asset class. Quinn’s standaardkader:\n"
            "- Zie crypto als hoog-risico satellietpositie, niet als kern van je portefeuille.\n"
            "- Gebruik betrouwbare exchanges en hardware wallets.\n"
            "- Bepaal vooraf een allocatieplafond (bijv. 3–10% van je totale vermogen), "
            "afhankelijk van je risicoprofiel."
        )

    if intent == "rates":
        return (
            "Rentes worden beïnvloed door centrale bank beleid, inflatie en groeiverwachtingen.\n"
            "- Hogere rente → leningen worden duurder, sparen wordt aantrekkelijker.\n"
            "- Lagere rente → goedkoop krediet, maar sparen levert minder op.\n"
            "Voor hypotheken en leningen is het belangrijk om looptijd, vaste vs. variabele rente "
            "en je inkomenszekerheid in kaart te brengen."
        )

    if intent == "portfolio":
        return (
            "Een portefeuille wordt vaak opgebouwd in lagen:\n"
            "1. **Kern** — brede, goed gespreide ETF’s of fondsen.\n"
            "2. **Satellieten** — thematische beleggingen (tech, duurzaamheid, EM, etc.).\n"
            "3. **Speculatief** — hoge risico posities zoals individuele groeiaandelen of crypto.\n\n"
            f"Met jouw huidige profiel (**{risk_profile}**) zou je kern waarschijnlijk het grootste deel vormen."
        )

    if intent == "risk":
        return (
            "Risicomanagement is een van de belangrijkste onderdelen van beleggen:\n"
            "- Stel duidelijke maximale drawdown-, positie- en portefeuillerisico’s.\n"
            "- Diversifieer over sectoren, regio’s en asset classes.\n"
            "- Herbalanceer periodiek zodat je risico niet ongemerkt oploopt.\n"
            "Quinn kan je helpen risico’s conceptueel beter te begrijpen, maar geen individuele posities aanbevelen."
        )

    if intent == "inflation":
        return (
            "Inflatie vermindert de koopkracht van je geld. Beleggers gebruiken vaak:\n"
            "- Aandelen (bedrijven kunnen prijzen verhogen)\n"
            "- Vastgoed\n"
            "- Inflatiegerelateerde obligaties\n"
            "Let wel op: dit zijn algemene voorbeelden, geen persoonlijk advies."
        )

    if intent == "advice":
        return (
            "Belangrijk: Quinn geeft **geen persoonlijk financieel advies**. "
            "Wat ik wél kan doen is kaders en scenario’s schetsen zodat jij beter onderbouwde keuzes kunt maken. "
            "Vertel bijvoorbeeld:\n"
            "- Je beleggingshorizon (kort <3 jaar, middellang 3–7 jaar, lang >7 jaar)\n"
            "- Hoe je jezelf zou omschrijven qua risico (Defensief / Neutraal / Offensief)\n"
            "- Of je vooral wilt opbouwen, beschermen of optimaliseren."
        )

    # Algemene fallback
    return (
        "Interessante vraag! Ik kan je helpen met uitleg over aandelen, ETF’s, crypto, rente, "
        "portefeuille-opbouw, risicomanagement en scenario’s. Kun je iets specifieker aangeven "
        "welk thema je wilt uitdiepen?"
    )


# =========================================================
# SIDEBAR — Quinn instellingen
# =========================================================
with st.sidebar:
    st.markdown(
        f"<h2 style='color:{PRIMARY};'>💬 Quinn</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color:{SECONDARY2};'>FinTech Assistant met focus op helderheid, structuur en "
        f"risicobewustzijn. "
        f"Deze app is educatief en géén persoonlijk financieel advies.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("Risicoprofiel")
    risk = st.radio(
        "Kies je globale risicoprofiel:",
        ["Defensief", "Neutraal", "Offensief"],
        index=["Defensief", "Neutraal", "Offensief"].index(st.session_state["risk_profile"]),
        label_visibility="collapsed",
    )
    st.session_state["risk_profile"] = risk

    st.markdown("---")
    st.subheader("Navigatie")
    page = st.radio(
        "Ga naar:",
        ["Chat met Quinn", "Market overview (demo)", "Scenario tools"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        "<p class='disclaimer'>Let op: Quinn geeft geen persoonlijk advies, doet geen aanbevelingen "
        "voor specifieke producten en kent jouw volledige financiële situatie niet. "
        "Zie dit als educatieve ondersteuning.</p>",
        unsafe_allow_html=True,
    )

# =========================================================
# PAGINA 1 — CHAT MET QUINN
# =========================================================
if page == "Chat met Quinn":
    st.markdown(
        f"""
        <h1 style='color:{PRIMARY};'>Chat met Quinn</h1>
        <p style='color:{SECONDARY2};'>
        Stel je vragen over beleggen, risico, portefeuille-structuur of macro-economie.
        Quinn reageert in duidelijke, compacte antwoorden.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Quick suggestions
    st.write("**Snelkoppelingen:**")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    quick_qs = {
        "Hoe bouw ik een portefeuille?": qcol1,
        "Wat is een defensief profiel?": qcol2,
        "Hoe kijk je naar crypto?": qcol3,
        "Wat betekent inflatie voor mij?": qcol4,
    }

    clicked_quick = None
    for text, col in quick_qs.items():
        with col:
            if st.button(text, key=f"quick_{text}"):
                clicked_quick = text

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat window
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state["messages"]:
        bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
        st.markdown(
            f"<div class='{bubble_class}'>{msg['text']}<div class='timestamp'>{msg['time']}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 1])
        with col1:
            user_input = st.text_input(
                "",
                placeholder="Stel je vraag aan Quinn…",
                label_visibility="collapsed",
            )
        with col2:
            send = st.form_submit_button("📨")

    # Als quick button gebruikt is, overschrijf input
    if clicked_quick:
        user_input = clicked_quick
        send = True  # direct versturen

    # Message handling
    if send and user_input and user_input.strip():
        now = datetime.now().strftime("%H:%M")

        st.session_state["messages"].append(
            {"role": "user", "text": user_input, "time": now}
        )

        reply = quinn_reply(user_input, st.session_state["risk_profile"])

        st.session_state["messages"].append(
            {"role": "bot", "text": reply, "time": now}
        )

        st.experimental_rerun()

# =========================================================
# PAGINA 2 — MARKET OVERVIEW (DEMO DATA)
# =========================================================
elif page == "Market overview (demo)":
    st.markdown(
        f"""
        <h1 style='color:{PRIMARY};'>Market overview (demo)</h1>
        <p style='color:{SECONDARY2};'>
        Dit dashboard gebruikt gesimuleerde data om te laten zien hoe een toekomstige Quinn-marktmodule eruit kan zien.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Demo time series (30 dagen)
    days = 30
    dates = [date.today() - timedelta(days=d) for d in range(days)][::-1]

    np.random.seed(42)
    base_index = np.cumsum(np.random.normal(0.2, 1.0, days)) + 100
    tech_index = np.cumsum(np.random.normal(0.4, 1.5, days)) + 120
    crypto_index = np.cumsum(np.random.normal(0.8, 3.0, days)) + 80

    df = pd.DataFrame(
        {
            "Datum": dates,
            "Global Equity Index": base_index,
            "Tech Growth Index": tech_index,
            "Crypto Basket": crypto_index,
        }
    ).set_index("Datum")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Synthetische indexontwikkeling (30 dagen)")
        st.line_chart(df)

    with col2:
        st.subheader("Indicatieve asset allocatie (demo)")

        alloc = pd.DataFrame(
            {
                "Asset": ["Equities", "Bonds", "Cash", "Alternatives"],
                "Percentage": [55, 25, 10, 10],
            }
        )

        st.bar_chart(
            alloc.set_index("Asset")
        )

        st.markdown(
            "<p class='metric-label'>Bovenstaande verdeling is illustratief en géén advies.</p>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Global Equity Index", f"{df['Global Equity Index'].iloc[-1]:.1f}", f"{df['Global Equity Index'].iloc[-1]-df['Global Equity Index'].iloc[0]:+.1f}")
    with col4:
        st.metric("Tech Growth Index", f"{df['Tech Growth Index'].iloc[-1]:.1f}", f"{df['Tech Growth Index'].iloc[-1]-df['Tech Growth Index'].iloc[0]:+.1f}")
    with col5:
        st.metric("Crypto Basket", f"{df['Crypto Basket'].iloc[-1]:.1f}", f"{df['Crypto Basket'].iloc[-1]-df['Crypto Basket'].iloc[0]:+.1f}")

    st.markdown(
        "<p class='disclaimer'>Alle cijfers hierboven zijn willekeurig gegenereerd en dienen alleen "
        "om de layout te illustreren.</p>",
        unsafe_allow_html=True,
    )

# =========================================================
# PAGINA 3 — SCENARIO TOOLS
# =========================================================
else:
    st.markdown(
        f"""
        <h1 style='color:{PRIMARY};'>Scenario tools</h1>
        <p style='color:{SECONDARY2};'>
        Speel met eenvoudige scenario’s: rendement op termijn en maandelijkse inleg (DCA).
        Deze tools zijn educatief en maken gebruik van basisformules.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["📈 Eindwaarde berekening", "💸 DCA-simulatie"])

    # ---- Tab 1: Future Value ----
    with tab1:
        st.subheader("Eindwaarde bij vast jaarlijks rendement")

        c1, c2, c3 = st.columns(3)
        with c1:
            start_capital = st.number_input(
                "Startkapitaal (€)",
                min_value=0.0,
                value=10000.0,
                step=500.0,
            )
        with c2:
            yearly_return = st.number_input(
                "Verwacht jaarlijks rendement (%)",
                min_value=-50.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
            )
        with c3:
            years = st.number_input(
                "Aantal jaren",
                min_value=1,
                max_value=50,
                value=10,
                step=1,
            )

        if st.button("Bereken eindwaarde"):
            r = yearly_return / 100
            final_value = start_capital * ((1 + r) ** years)

            st.success(f"Verwachte eindwaarde na {years} jaar: **€ {final_value:,.2f}**")

            # Tijdlijn
            values = [start_capital * ((1 + r) ** t) for t in range(years + 1)]
            years_list = list(range(years + 1))
            chart_df = pd.DataFrame({"Jaar": years_list, "Waarde": values}).set_index(
                "Jaar"
            )
            st.line_chart(chart_df)

            st.markdown(
                "<p class='disclaimer'>Let op: dit is een vereenvoudigd voorbeeld met een vast rendement en "
                "houdt geen rekening met inflatie, belastingen of risico.</p>",
                unsafe_allow_html=True,
            )

    # ---- Tab 2: DCA Simulation ----
    with tab2:
        st.subheader("DCA — maandelijks investeren")

        c1, c2, c3 = st.columns(3)
        with c1:
            monthly_invest = st.number_input(
                "Maandelijkse inleg (€)",
                min_value=0.0,
                value=250.0,
                step=50.0,
            )
        with c2:
            yearly_return_dca = st.number_input(
                "Verwacht effectief jaarrendement (%)",
                min_value=-50.0,
                max_value=50.0,
                value=6.0,
                step=0.5,
            )
        with c3:
            years_dca = st.number_input(
                "Duur in jaren",
                min_value=1,
                max_value=50,
                value=15,
                step=1,
            )

        if st.button("Simuleer DCA"):
            months = years_dca * 12
            r_month = (1 + yearly_return_dca / 100) ** (1 / 12) - 1

            values = []
            total_invested = []
            current_value = 0.0
            invested = 0.0

            for m in range(months + 1):
                if m > 0:
                    invested += monthly_invest
                    current_value = (current_value + monthly_invest) * (1 + r_month)
                values.append(current_value)
                total_invested.append(invested)

            df_dca = pd.DataFrame(
                {
                    "Maand": list(range(months + 1)),
                    "Portefeuillewaarde": values,
                    "Totaal ingelegd": total_invested,
                }
            ).set_index("Maand")

            st.line_chart(df_dca[["Portefeuillewaarde", "Totaal ingelegd"]])

            st.success(
                f"Na {years_dca} jaar heb je in totaal **€ {invested:,.2f}** ingelegd.\n\n"
                f"De gesimuleerde portefeuillewaarde is **€ {current_value:,.2f}**."
            )

            st.markdown(
                "<p class='disclaimer'>Ook dit is een vereenvoudigd voorbeeld. "
                "Werkelijke rendementen kunnen fors afwijken. Zie dit uitsluitend als educatieve visualisatie.</p>",
                unsafe_allow_html=True,
            )

