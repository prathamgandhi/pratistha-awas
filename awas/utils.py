from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageBreak, Table, NextPageTemplate, Image, HRFlowable, Spacer
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.lib.units import cm
from reportlab.lib import colors
from functools import partial
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

import random
from django.utils import timezone, dateformat
from django.db.models import Sum

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='org_name',
                          parent=styles['Normal'],
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=12,
                          leading=13,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=1.0,))

styles.add(ParagraphStyle(name='org_address',
                          parent=styles['Normal'],
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=8,
                          leading=8,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=1.0,))

styles.add(ParagraphStyle(name='doc_title',
                          parent=styles['Heading2'],
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontsize=30,
                          leading=16,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,))
styles.add(ParagraphStyle(name='NormalBold',
                          parent=styles['Normal'],
                          fontSize=10,
                          fontName='Helvetica-Bold',))
styles.add(ParagraphStyle(name='NormalSmall',
                          parent=styles['Normal'],
                          fontSize=9,
                          wordWrap='LTR',))

class MyDocTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

        template_NormalPage = PageTemplate('NormalPage',
                                [Frame(1.75*cm, 2.5*cm, 17.5*cm, 23*cm, id='F1')],
                                onPage=partial(header_and_footer,
                                header_content=header_content,
                                footer_content=footer_content))
        self.addPageTemplates([template_NormalPage])

'-----------------------------------------------------------------------------'
'Header and Footer'
'-----------------------------------------------------------------------------'
def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin-22.4, doc.height + doc.bottomMargin + doc.topMargin - h-25)
    canvas.restoreState()

def footer(canvas, doc, content):
    drawPageNumber(canvas, doc)
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.bottomMargin)
    content.drawOn(canvas, doc.leftMargin-22.4, h)
    canvas.restoreState()

def header_and_footer(canvas, doc, header_content, footer_content):
    header(canvas, doc, header_content)
    footer(canvas, doc, footer_content)

def drawPageNumber(canvas, doc):
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica",11)
    canvas.drawCentredString(17.4*cm, 1.35*cm, 'Page '+str(pageNumber))

def PageNumber(canvas, doc):
    return(canvas.getPageNumber())

footer_center_text=dateformat.format(timezone.localtime(timezone.now()), 'Y-m-d H:i:s',)
logo_path = "logo.png"

    
def create_deco(report_title):
    '-----------------------------------------------------------------------------'
    'Header'
    '-----------------------------------------------------------------------------'
    org_name = (("Shree 1008 Shantinath Digamber Jinbimb Panchkalyanak Pratishtha Mahotsav"))
    org_name_para = Paragraph(org_name, styles['org_name'])
    org_address = (("Pratishtha Venue: Hansraj Morarji Public School Campus, D.N.Road, Munshi Nagar, Andheri(West), Mumbai-400 058 Helpdesk ☎: +91 7045117135 / 7045117136 | : awas@parlajinmandir.org"))
    org_address_para = Paragraph(org_address, styles['org_address'])
    title = ((report_title))
    title_para = Paragraph(title, styles['doc_title'])
    A='Author'
    logo_to_use = Image(logo_path, width=1.5*cm, height=2.53*cm)
    Header_table_data=[
                        [logo_to_use, org_name_para, logo_to_use],
                        ['', org_address_para, ''],
                        ['', title_para, ''],
                    ]
    relative_colWidths = [20, 80, 20]
    page_width, page_height = letter
    col_widths = [width/100 * page_width for width in relative_colWidths]
    Header_table=Table(Header_table_data,colWidths=[2.6*cm, 12.5*cm ,2.6*cm],rowHeights=[1.0*cm, 1.0*cm, 1.0*cm],style=[
    ('VALIGN',(1,0),(1,2),'MIDDLE'),
    ('SPAN',(0,0),(0,2)),
    ('SPAN',(2,0),(2,2)),
    ('ALIGN', (0,0), (2,0), 'CENTER'),
    ('VALIGN', (0,0), (2,0), 'MIDDLE'),
    ('TEXTCOLOR',(0,0),(-1,-1),colors.Color(49/255,71/255,137/255))
    ])
    '-----------------------------------------------------------------------------'
    'Footer'
    '-----------------------------------------------------------------------------'
    Footer_caption=(footer_center_text)
    Seitenzahl=''
    Footerer_ID=Seitenzahl
    
    Footer_table_data=[[footer_center_text,"",Footerer_ID]]
    Footer_table=Table(Footer_table_data,colWidths=[4*cm,9.5*cm,4*cm],rowHeights=[1*cm],style=[
    ('ALIGN',(0,0),(-1,-1),'RIGHT'),
    ('VALIGN',(0,0),(2,0),'MIDDLE'),
    ('ALIGN',(0,0),(3,0),'CENTER'),
    ])
    
    footer_content = Footer_table
    header_content = Header_table
    return header_content, footer_content 

class ReportTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

        header_content, footer_content = create_deco(kw['report_title'])
        template_NormalPage = PageTemplate('NormalPage',
                                [Frame(1.75*cm, 2.5*cm, 17.5*cm, 21*cm, id='F1')],
                                onPage=partial(header_and_footer,
                                header_content=header_content,
                                footer_content=footer_content))

        self.addPageTemplates([template_NormalPage])

def fill_accomodation_slip(queryset, story):
    location = queryset.first()
    location_data_table = [
        [
            Paragraph('Address', styles['NormalBold']),
            Paragraph(f"{str(location.description if location.description is not None else '--')}\n{str(location.address) if location.address is not None else '--'}", styles['Normal']),
            Paragraph('Mode of Transport', styles['NormalBold']),
            Paragraph(str(location.transport if location.transport is not None else '--'), styles['Normal']),
        ],
        [
            Paragraph('Checkin/Checkout time', styles['NormalBold']),
            Paragraph(f'{location.checkin_time if location.checkin_time is not None else "--"}/{location.checkout_time if location.checkout_time is not None else "--"}', styles['Normal']),
            Paragraph(f'Map Link', styles['NormalBold']),
            Paragraph(str(location.map_link if location.map_link is not None else '--'), styles['Normal']),
        ],
        [
            Paragraph('Awas Incharge', styles['NormalBold']),
            Paragraph(str(location.awas_incharge if location.awas_incharge is not None else '--'), styles['Normal']),
            Paragraph('Key/Lock No.', styles['NormalBold']),
            Paragraph(str(location.lock_no if location.lock_no is not None else '--'), styles['Normal']),
        ],
    ]
    story.append(
        Table(location_data_table,colWidths=[5*cm, 5*cm, 5*cm, 5*cm],rowHeights=[2*cm]*3,style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
        ])
    )

    story.append(Spacer(20*cm, 1*cm))
    guests = location.guest_set.all()
    if guests.count() == 0:
        return



    guest_data_header = [['Reg#', 'Name', 'City', 'Mobile No.', 'Arrival', 'Depart', 'Persons'],]
    guest_data_header = [
            [Paragraph(cell, styles['NormalBold']) for cell in row] for row in guest_data_header 
        ]


    guest_rows = [
            [
                Paragraph(str(guest.ext_reg_no), styles['NormalSmall']),
                Paragraph(str(guest.guest_name), styles['NormalSmall']),
                Paragraph(str(guest.city), styles['NormalSmall']),
                Paragraph(str(guest.mobile_no), styles['NormalSmall']),
                Paragraph(str(guest.arrival_date), styles['NormalSmall']),
                Paragraph(str(guest.departure_date), styles['NormalSmall']),
                Paragraph(str(guest.no_of_persons), styles['NormalSmall']),
            ] 
                for guest in guests
        ]
    

    data_to_add = guest_data_header
    data_to_add.extend(guest_rows)
    tab = Table(data_to_add,colWidths=[1.4*cm,5.5*cm,2.5*cm,2.5*cm,3*cm,3*cm,2*cm],rowHeights=[1*cm]*len(data_to_add),style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('ALIGN',(5,0),(6,0),'CENTER'),
            ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
            ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ('FONTSIZE',(0,0),(-1,-1),9),
            # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.lightgrey]),
        ]
    )
    story.append(tab)

def fill_location_capacity_report(queryset, story):
    table_column_data = [['Location Description', 'Capacity', 'Reserved', 'Balanced']]
    bold_table_column_data = [
            [Paragraph(cell, styles['NormalBold']) for cell in row] for row in table_column_data
        ]
    story.append(
        Table(bold_table_column_data,colWidths=[10.5*cm,2.5*cm,2.5*cm,2.5*cm],rowHeights=[1*cm],style=[
            #('GRID',(0,0),(-1,-1),1,colors.black),
                ('ALIGN',(0,1),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
                ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
                ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ])
    )

    location_rows = [
        [
            Paragraph(str(location.description), styles['NormalSmall']),
            Paragraph(str(location.capacity), styles['NormalSmall']),
            Paragraph(str(location.reserved), styles['NormalSmall']),
            Paragraph(str(location.capacity-location.reserved), styles['NormalSmall']),
        ]
        for location in queryset
    ]
    capacity_total = queryset.aggregate(Sum('capacity'))['capacity__sum']
    reserved_total = queryset.aggregate(Sum('reserved'))['reserved__sum']
    balance_total = capacity_total - reserved_total
    location_rows.append(
        [
            Paragraph('Grand Total', styles['NormalSmall']),
            Paragraph(str(capacity_total), styles['NormalSmall']),
            Paragraph(str(reserved_total), styles['NormalSmall']),
            Paragraph(str(balance_total), styles['NormalSmall']),
        ]
    )
    tab = Table(location_rows, colWidths=[10.5*cm,2.5*cm,2.5*cm,2.5*cm],rowHeights=[1*cm]*len(location_rows),style=[
            # ('GRID',(0,0),(-1,-1),1,colors.black),
            ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
            ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.lightgrey]),
        ]
    )
    story.append(tab)


def fill_guest_wise_allotment(queryset, story):
    table_column_data = [['Name', 'City', 'Location', 'Mobile No.', 'Reg No.', 'Persons'],]
    bold_table_column_data = [
            [Paragraph(cell, styles['NormalBold']) for cell in row] for row in table_column_data
        ]
    story.append(
        Table(bold_table_column_data,colWidths=[5.5*cm,2.5*cm,3.5*cm,3*cm,1.5*cm,2.5*cm],rowHeights=[1*cm],style=[
            #('GRID',(0,0),(-1,-1),1,colors.black),
                ('ALIGN',(0,1),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
                ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
                ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ])
        )

    guest_rows = [
        [
            Paragraph(str(guest.guest_name), styles['NormalSmall']),
            Paragraph(str(guest.city), styles['NormalSmall']),
            Paragraph(str(guest.location.description if guest.location is not None else ""), styles['NormalSmall']),
            Paragraph(str(guest.mobile_no), styles['NormalSmall']),
            Paragraph(str(guest.ext_reg_no), styles['NormalSmall']),
            Paragraph(str(guest.no_of_persons), styles['NormalSmall']),
        ]
        for guest in queryset
    ]
    tab = Table(guest_rows,colWidths=[4.5*cm,2.5*cm,4.5*cm,3*cm,1.5*cm,2.5*cm],rowHeights=[1*cm]*len(guest_rows),style=[
            # ('GRID',(0,0),(-1,-1),1,colors.black),
            ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
            ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.lightgrey, colors.white]),
        ]
    )
    story.append(tab)
    story.append(Spacer(20*cm, 1*cm))
    total_person_count = queryset.aggregate(Sum('no_of_persons'))['no_of_persons__sum']
    story.append(Paragraph(f"Total Persons Reserved : {total_person_count}"))

def fill_location_wise_allotment(queryset, story):
    table_column_data = [['Location', '', '', '', '', '', ''],
                     ['Reg#', 'Name', 'City', 'Mobile No.', 'Arrival', 'Depart', 'Persons'],]
    bold_table_column_data = [
            [Paragraph(cell, styles['NormalBold']) for cell in row] for row in table_column_data
        ]
    story.append(
        Table(bold_table_column_data,colWidths=[1.4*cm,4.5*cm,2.5*cm,2.5*cm,3*cm,3*cm,2*cm],rowHeights=[1*cm,1*cm],style=[
            #('GRID',(0,0),(-1,-1),1,colors.black),
                ('SPAN',(0,0),(6,0)),
                ('ALIGN',(0,1),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
                ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
                ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
            ])
        )

    
    for query in queryset:
        location_row = [
            [Paragraph(query.description, styles['NormalBold']), '', '',Paragraph(f'Capacity : {query.capacity}', styles['NormalBold']), '', Paragraph(f'Total Reserved : {query.reserved}', styles['NormalBold']), ''],
        ]
        guests = query.guest_set.all()
        if guests.count() == 0:
            continue
        guest_rows = [
            [
                Paragraph(str(guest.ext_reg_no), styles['NormalSmall']),
                Paragraph(str(guest.guest_name), styles['NormalSmall']),
                Paragraph(str(guest.city), styles['NormalSmall']),
                Paragraph(str(guest.mobile_no), styles['NormalSmall']),
                Paragraph(str(guest.arrival_date), styles['NormalSmall']),
                Paragraph(str(guest.departure_date), styles['NormalSmall']),
                Paragraph(str(guest.no_of_persons), styles['NormalSmall']),
            ] 
                for guest in guests
        ]
        data_to_add = location_row
        data_to_add.extend(guest_rows)
        tab = Table(data_to_add,colWidths=[1.4*cm,4.5*cm,2.5*cm,2.5*cm,3*cm,3*cm,1.5*cm],rowHeights=[1*cm]*len(data_to_add),style=[
                # ('GRID',(0,0),(-1,-1),1,colors.black),
                ('SPAN',(0,0),(2,0)),
                ('SPAN',(3,0),(4,0)),
                ('SPAN',(5,0),(6,0)),
                ('ALIGN',(5,0),(6,0),'CENTER'),
                ('LINEBELOW',(0,-1),(-1,-1),0.5,colors.black),
                ('LINEABOVE',(0,0),(-1,0),0.5,colors.black),
                ('FONTSIZE',(0,0),(-1,-1),9),
                ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.lightgrey]),
            ]
        )
        story.append(tab)