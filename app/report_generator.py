"""
Generatore di Report PDF per il sistema di gestione didattica
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
from collections import defaultdict

class ReportGenerator:
    """Classe per la generazione di report PDF"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura stili personalizzati"""
        # Titolo principale
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1976d2'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Sottotitolo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#424242'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Info header
        self.styles.add(ParagraphStyle(
            name='InfoText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=6
        ))

    def generate_report_voti(self, classe, studenti_voti, materia=None):
        """
        Genera report registro voti per classe

        Args:
            classe: Oggetto classe
            studenti_voti: Lista di dict con studenti e relativi voti
            materia: Oggetto materia (opzionale)
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []

        # Titolo
        if materia:
            title = f"Registro Voti - {classe.nome} - {materia.nome}"
        else:
            title = f"Registro Voti - {classe.nome}"

        elements.append(Paragraph(title, self.styles['CustomTitle']))

        # Info generazione
        data_generazione = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        elements.append(Paragraph(
            f"Report generato il {data_generazione}",
            self.styles['InfoText']
        ))
        elements.append(Spacer(1, 20))

        # Prepara dati tabella
        if not studenti_voti:
            elements.append(Paragraph(
                "Nessun voto registrato per questa selezione.",
                self.styles['Normal']
            ))
        else:
            # Header tabella
            data = [['Studente', 'Materia', 'Voto', 'Tipo', 'Data', 'Note']]

            # Aggiungi righe
            for item in studenti_voti:
                data.append([
                    f"{item['cognome']} {item['nome']}",
                    item['materia_nome'],
                    str(item['voto']),
                    item['tipo'] or '-',
                    datetime.strptime(item['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    item['note'] or '-'
                ])

            # Crea tabella
            table = Table(data, colWidths=[4.5*cm, 4*cm, 2*cm, 2.5*cm, 2.5*cm, 6*cm])

            # Stile tabella
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Voto centrato
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))

            elements.append(table)

            # Statistiche
            elements.append(Spacer(1, 30))
            elements.append(Paragraph(
                f"Totale voti registrati: {len(studenti_voti)}",
                self.styles['CustomSubtitle']
            ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_report_presenze(self, classe, presenze_data, data_inizio=None, data_fine=None):
        """
        Genera report presenze per classe

        Args:
            classe: Oggetto classe
            presenze_data: Lista di dict con presenze
            data_inizio: Data inizio periodo (opzionale)
            data_fine: Data fine periodo (opzionale)
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []

        # Titolo
        title = f"Registro Presenze - {classe.nome}"
        elements.append(Paragraph(title, self.styles['CustomTitle']))

        # Info periodo
        periodo_text = "Anno scolastico completo"
        if data_inizio and data_fine:
            periodo_text = f"Periodo: {data_inizio.strftime('%d/%m/%Y')} - {data_fine.strftime('%d/%m/%Y')}"
        elif data_inizio:
            periodo_text = f"Dal {data_inizio.strftime('%d/%m/%Y')}"
        elif data_fine:
            periodo_text = f"Fino al {data_fine.strftime('%d/%m/%Y')}"

        elements.append(Paragraph(periodo_text, self.styles['InfoText']))

        data_generazione = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        elements.append(Paragraph(
            f"Report generato il {data_generazione}",
            self.styles['InfoText']
        ))
        elements.append(Spacer(1, 20))

        # Prepara dati tabella
        if not presenze_data:
            elements.append(Paragraph(
                "Nessuna presenza registrata per questa selezione.",
                self.styles['Normal']
            ))
        else:
            # Header tabella
            data = [['Data', 'Studente', 'Tipo', 'Ora Ingresso', 'Ora Uscita', 'Giustificata', 'Note']]

            # Aggiungi righe
            for item in presenze_data:
                tipo_label = item['tipo'].replace('_', ' ').title()
                giust_label = 'Sì' if item['giustificata'] else 'No'

                data.append([
                    datetime.strptime(item['data'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                    f"{item['cognome']} {item['nome']}",
                    tipo_label,
                    item['ora_ingresso'] or '-',
                    item['ora_uscita'] or '-',
                    giust_label,
                    item['note'] or '-'
                ])

            # Crea tabella
            table = Table(data, colWidths=[2.5*cm, 4.5*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 5*cm])

            # Stile tabella
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # Data centrata
                ('ALIGN', (5, 0), (5, -1), 'CENTER'),  # Giustificata centrata
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))

            elements.append(table)

            # Statistiche
            elements.append(Spacer(1, 30))
            stats_title = Paragraph("Statistiche", self.styles['CustomSubtitle'])
            elements.append(stats_title)

            # Conta tipi
            tipo_counts = defaultdict(int)
            for item in presenze_data:
                tipo_counts[item['tipo']] += 1

            stats_text = f"Totale registrazioni: {len(presenze_data)}<br/>"
            stats_text += f"Presenti: {tipo_counts.get('presente', 0)}<br/>"
            stats_text += f"Assenti: {tipo_counts.get('assente', 0)}<br/>"
            stats_text += f"Ritardi: {tipo_counts.get('ritardo', 0)}<br/>"
            stats_text += f"Uscite anticipate: {tipo_counts.get('uscita_anticipata', 0)}"

            elements.append(Paragraph(stats_text, self.styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_pagella(self, studente, voti_per_materia, periodo='annuale'):
        """
        Genera pagella studente

        Args:
            studente: Oggetto studente
            voti_per_materia: Dict con materie e voti
            periodo: 'annuale', 'primo', 'secondo'
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []

        # Titolo
        periodo_map = {
            'annuale': 'Anno Scolastico',
            'primo': 'Primo Quadrimestre',
            'secondo': 'Secondo Quadrimestre'
        }

        elements.append(Paragraph("PAGELLA SCOLASTICA", self.styles['CustomTitle']))
        elements.append(Paragraph(periodo_map.get(periodo, 'Anno Scolastico'), self.styles['CustomSubtitle']))
        elements.append(Spacer(1, 20))

        # Info studente
        info_studente = f"""
        <b>Studente:</b> {studente.cognome} {studente.nome}<br/>
        <b>Classe:</b> {studente.classe_nome or 'Non assegnata'}<br/>
        <b>Data di nascita:</b> {studente.data_nascita.strftime('%d/%m/%Y') if studente.data_nascita else 'N/D'}<br/>
        """
        elements.append(Paragraph(info_studente, self.styles['Normal']))
        elements.append(Spacer(1, 30))

        # Tabella voti
        if not voti_per_materia:
            elements.append(Paragraph(
                "Nessun voto registrato per questo periodo.",
                self.styles['Normal']
            ))
        else:
            data = [['Materia', 'Media', 'N° Voti']]

            media_totale = 0
            for materia_nome, info in voti_per_materia.items():
                media = info['media']
                num_voti = info['numero_voti']
                data.append([
                    materia_nome,
                    f"{media:.2f}",
                    str(num_voti)
                ])
                media_totale += media

            # Calcola media generale
            if len(voti_per_materia) > 0:
                media_generale = media_totale / len(voti_per_materia)
                data.append(['', '', ''])  # Riga vuota
                data.append(['MEDIA GENERALE', f"{media_generale:.2f}", ''])

            # Crea tabella
            table = Table(data, colWidths=[10*cm, 3*cm, 3*cm])

            # Stile tabella
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.white),
                ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')]),
                # Stile riga media generale
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e3f2fd')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 11),
            ]))

            elements.append(table)

        # Footer
        elements.append(Spacer(1, 40))
        data_generazione = datetime.now().strftime("%d/%m/%Y")
        elements.append(Paragraph(
            f"Documento generato il {data_generazione}",
            self.styles['InfoText']
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_statistiche_classe(self, classe, statistiche):
        """
        Genera report statistiche classe

        Args:
            classe: Oggetto classe
            statistiche: Dict con statistiche varie
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        elements = []

        # Titolo
        elements.append(Paragraph(
            f"Statistiche Classe {classe.nome}",
            self.styles['CustomTitle']
        ))

        data_generazione = datetime.now().strftime("%d/%m/%Y alle %H:%M")
        elements.append(Paragraph(
            f"Report generato il {data_generazione}",
            self.styles['InfoText']
        ))
        elements.append(Spacer(1, 30))

        # Statistiche generali
        elements.append(Paragraph("Informazioni Generali", self.styles['CustomSubtitle']))

        info_generale = f"""
        <b>Numero studenti:</b> {statistiche['numero_studenti']}<br/>
        <b>Media classe:</b> {statistiche['media_classe']:.2f}<br/>
        <b>Totale voti registrati:</b> {statistiche['totale_voti']}<br/>
        <b>Totale presenze registrate:</b> {statistiche['totale_presenze']}<br/>
        """
        elements.append(Paragraph(info_generale, self.styles['Normal']))
        elements.append(Spacer(1, 30))

        # Medie per materia
        if statistiche.get('medie_per_materia'):
            elements.append(Paragraph("Medie per Materia", self.styles['CustomSubtitle']))
            elements.append(Spacer(1, 10))

            data = [['Materia', 'Media Classe', 'N° Voti']]

            for materia, info in statistiche['medie_per_materia'].items():
                data.append([
                    materia,
                    f"{info['media']:.2f}",
                    str(info['numero_voti'])
                ])

            table = Table(data, colWidths=[10*cm, 3*cm, 3*cm])

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))

            elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer
