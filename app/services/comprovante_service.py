from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image as RLImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
import io
import os

CLINICA = {
    "nome": "Clínica Saúde & Vida",
    "rua": "Rua Coronel Adauto, 142 — Centro",
    "cidade": "Guarabira — PB, 58200-000",
    "cnpj": "CNPJ: 12.345.678/0001-99",
}

AZUL_ESCURO  = colors.HexColor("#042C53")
AZUL_MEDIO   = colors.HexColor("#185FA5")
AZUL_CLARO   = colors.HexColor("#E6F1FB")
AZUL_BORDA   = colors.HexColor("#B5D4F4")
VERDE_BG     = colors.HexColor("#EAF3DE")
VERDE_TEXTO  = colors.HexColor("#3B6D11")
CINZA        = colors.HexColor("#5F5E5A")
CINZA_CLARO  = colors.HexColor("#d3d1c7")

def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_data(data) -> str:
    if not data:
        return "—"
    try:
        return datetime.fromisoformat(str(data)).strftime("%d/%m/%Y")
    except:
        return str(data)

def formatar_data_hora(data) -> str:
    if not data:
        return "—"
    try:
        return datetime.fromisoformat(str(data)).strftime("%d/%m/%Y às %H:%M")
    except:
        return str(data)

def gerar_pdf(paciente: dict, consulta: dict, usuario: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    estilo_normal  = ParagraphStyle("normal", fontName="Helvetica", fontSize=10, textColor=colors.HexColor("#2c2c2a"))
    estilo_label   = ParagraphStyle("label",  fontName="Helvetica", fontSize=10, textColor=CINZA)
    estilo_bold    = ParagraphStyle("bold",   fontName="Helvetica-Bold", fontSize=10, textColor=colors.HexColor("#2c2c2a"))
    estilo_titulo  = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=8, textColor=AZUL_MEDIO, spaceAfter=6)
    estilo_rodape  = ParagraphStyle("rodape", fontName="Helvetica", fontSize=8, textColor=CINZA)

    elementos = []

    # LOGO
    caminho_logo = os.path.join(os.path.dirname(__file__), "../templates/img/logo.png")
    if os.path.exists(caminho_logo):
        logo = RLImage(caminho_logo, width=2*cm, height=2*cm)
    else:
        logo = Paragraph("[Logo]", ParagraphStyle("logo", fontName="Helvetica", fontSize=9, textColor=AZUL_MEDIO, alignment=TA_CENTER))

    # HEADER
    header_data = [[
        Table([
            [Paragraph(f"<b>{CLINICA['nome']}</b>", ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, textColor=AZUL_ESCURO))],
            [Paragraph(CLINICA["rua"],    estilo_label)],
            [Paragraph(CLINICA["cidade"], estilo_label)],
            [Paragraph(CLINICA["cnpj"],   estilo_label)],
        ], colWidths=[11*cm]),
        logo
    ]]
    header_table = Table(header_data, colWidths=[13*cm, 3*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_CLARO),
        ("BOX",        (0,0), (-1,-1), 0.5, AZUL_BORDA),
        ("ROUNDEDCORNERS", [8]),
        ("VALIGN",     (0,0), (-1,-1), "TOP"),
        ("PADDING",    (0,0), (-1,-1), 12),
        ("ALIGN",      (1,0), (1,0),   "CENTER"),
    ]))
    elementos.append(header_table)
    elementos.append(Spacer(1, 0.2*cm))

    # FAIXA AZUL
    faixa_data = [[
        Paragraph("COMPROVANTE DE CONSULTA", ParagraphStyle("faixa", fontName="Helvetica-Bold", fontSize=9, textColor=AZUL_CLARO)),
        Paragraph(f"#{consulta['id']} · {formatar_data(consulta['data_consulta'])}", ParagraphStyle("num", fontName="Helvetica", fontSize=9, textColor=AZUL_BORDA, alignment=TA_RIGHT)),
    ]]
    faixa = Table(faixa_data, colWidths=[10*cm, 6*cm])
    faixa.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_MEDIO),
        ("PADDING",    (0,0), (-1,-1), 7),
    ]))
    elementos.append(faixa)
    elementos.append(Spacer(1, 0.4*cm))

    # CORPO — duas colunas
    def linha(label, valor, negrito=False):
        return [Paragraph(label, estilo_label), Paragraph(valor or "—", estilo_bold if negrito else estilo_normal)]

    paciente_dados = Table([
        [Paragraph("DADOS DO PACIENTE", estilo_titulo), ""],
        *[linha(*l) for l in [
            ("Nome",        paciente.get("nome_completo", ""), True),
            ("CPF",         formatar_cpf(paciente.get("cpf", ""))),
            ("Nascimento",  formatar_data(paciente.get("data_nascimento"))),
            ("Telefone",    paciente.get("telefone")),
            ("E-mail",      paciente.get("email")),
            ("Convênio",    paciente.get("convenio") or "Particular"),
        ]]
    ], colWidths=[2.8*cm, 5.2*cm])
    paciente_dados.setStyle(TableStyle([
        ("SPAN",    (0,0), (1,0)),
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    badge = Table([
        [Paragraph("Pago", ParagraphStyle("badge", fontName="Helvetica-Bold", fontSize=9, textColor=VERDE_TEXTO, alignment=TA_CENTER))]
    ], colWidths=[2*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), VERDE_BG),
        ("ROUNDEDCORNERS", [4]),
        ("PADDING", (0,0), (-1,-1), 3),
    ]))

    valor_formatado = f"R$ {consulta.get('valor', 0):.2f}".replace(".", ",")

    consulta_dados = Table([
        [Paragraph("DADOS DA CONSULTA", estilo_titulo), ""],
        *[linha(*l) for l in [
            ("Data",         formatar_data_hora(consulta.get("data_consulta")), True),
            ("Especialidade",consulta.get("especialidade")),
            ("Motivo",       consulta.get("motivo")),
            ("Valor",        valor_formatado, True),
            ("Operador",     usuario.get("nome")),
        ]],
        [Paragraph("Status", estilo_label), badge],
    ], colWidths=[2.8*cm, 5.2*cm])
    consulta_dados.setStyle(TableStyle([
        ("SPAN",    (0,0), (1,0)),
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 3),
        ("BOTTOMPADDING",(0,0), (-1,-1), 3),
    ]))

    corpo = Table([[paciente_dados, consulta_dados]], colWidths=[8.5*cm, 8.5*cm])
    corpo.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",  (1,0), (1,0), 16),
    ]))
    elementos.append(corpo)
    elementos.append(Spacer(1, 0.4*cm))

    # OBSERVAÇÕES
    elementos.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_CLARO))
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(Paragraph("OBSERVAÇÕES", estilo_titulo))
    elementos.append(Paragraph(consulta.get("observacoes") or "Nenhuma observação registrada.", estilo_normal))
    elementos.append(Spacer(1, 0.4*cm))

    # RODAPÉ
    elementos.append(HRFlowable(width="100%", thickness=0.5, color=CINZA_CLARO))
    elementos.append(Spacer(1, 0.3*cm))
    rodape = Table([[
        Paragraph(f"Documento gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", estilo_rodape),
        Paragraph(f"Enviado para {paciente.get('email', '—')}", ParagraphStyle("r", fontName="Helvetica", fontSize=8, textColor=CINZA, alignment=TA_RIGHT)),
    ]], colWidths=[8.5*cm, 8.5*cm])
    elementos.append(rodape)

    doc.build(elementos)
    buffer.seek(0)
    return buffer.read()