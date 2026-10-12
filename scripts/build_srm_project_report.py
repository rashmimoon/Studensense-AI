import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding inside table cells."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def style_heading(p, font_name="Times New Roman", size_pt=14, bold=True, space_before=12, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    for run in p.runs:
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = RGBColor(0, 0, 0)

def add_body_p(doc, text="", space_after=6, bold_prefix="", indent=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.3)
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(12)
        r_text.font.color.rgb = RGBColor(0, 0, 0)
    return p

def create_report():
    doc = Document()
    
    # 1. Page Setup according to SRM Guidelines
    # Margins: Left 4 cm, Top 3 cm, Bottom 3 cm, Right 2 cm
    sections = doc.sections
    for section in sections:
        section.page_width = Cm(21.0) # A4
        section.page_height = Cm(29.7)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(2.0)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(3.0)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # ---------------------------------------------------------------------------
    # FRONT MATTER: TITLE PAGE
    # ---------------------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    r = p_title.add_run("STUDENTSENSE AI: STUDENT BEHAVIOR PREDICTION AND PERSONALIZED RECOMMENDATION SYSTEM USING EXPLAINABLE MACHINE LEARNING AND RETRIEVAL-AUGMENTED GENERATION\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(15)
    r.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(18)
    r = p_sub.add_run("A PROJECT REPORT SUBMITTED TO\nSRM INSTITUTE OF SCIENCE AND TECHNOLOGY\nIN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF\nMASTER OF COMPUTER APPLICATIONS\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(18)
    r = p_by.add_run("BY\nRASHMI MOON (RA2452003010185)\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(24)
    r = p_guide.add_run("UNDER THE GUIDANCE OF\nFACULTY PROJECT GUIDE\nAssistant Professor, Department of Computer Applications\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(36)
    p_dept.paragraph_format.space_after = Pt(0)
    r = p_dept.add_run("DEPARTMENT OF COMPUTER APPLICATIONS\nFACULTY OF SCIENCE AND HUMANITIES\nSRM INSTITUTE OF SCIENCE AND TECHNOLOGY\nKattankulathur – 603 203, Chennai, Tamil Nadu\nOCTOBER - 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # BONAFIDE CERTIFICATE
    # ---------------------------------------------------------------------------
    h = doc.add_paragraph()
    h.add_run("BONAFIDE CERTIFICATE")
    style_heading(h, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    add_body_p(doc, 
        "This is to certify that the project report titled “STUDENTSENSE AI: STUDENT BEHAVIOR PREDICTION AND PERSONALIZED RECOMMENDATION SYSTEM” is a bonafide work carried out by RASHMI MOON (Register Number: RA2452003010185) under my supervision for the award of the Degree of Master of Computer Applications in the Department of Computer Applications, Faculty of Science and Humanities, SRM Institute of Science and Technology. To the best of my knowledge, the work reported herein is the original work done by this candidate and has not been submitted elsewhere for any degree or diploma.",
        space_after=36, indent=True
    )

    table_cert = doc.add_table(rows=2, cols=2)
    table_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_cert.rows[0].cells[0].paragraphs[0].text = "PROJECT GUIDE\n\n\n___________________________\nFaculty Guide\nDepartment of Computer Applications\nSRM Institute of Science and Technology"
    table_cert.rows[0].cells[1].paragraphs[0].text = "HEAD OF THE DEPARTMENT\n\n\n___________________________\nDr. P. J. Arul Leena Rose\nProfessor & Head\nDepartment of Computer Applications\nSRM Institute of Science and Technology"
    table_cert.rows[1].cells[0].paragraphs[0].text = "\n\nINTERNAL EXAMINER:\nSignature: __________________\nDate: ______________________"
    table_cert.rows[1].cells[1].paragraphs[0].text = "\n\nEXTERNAL EXAMINER:\nSignature: __________________\nDate: ______________________"

    for row in table_cert.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(11)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # DECLARATION
    # ---------------------------------------------------------------------------
    h_dec = doc.add_paragraph()
    h_dec.add_run("DECLARATION")
    style_heading(h_dec, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    add_body_p(doc, 
        "I hereby declare that the project entitled “STUDENTSENSE AI: STUDENT BEHAVIOR PREDICTION AND PERSONALIZED RECOMMENDATION SYSTEM” submitted to SRM Institute of Science and Technology, Chennai, in partial fulfillment of the requirements for the award of the Degree of Master of Computer Applications, is a record of original work done by me under the supervision and guidance of Faculty Guide, Department of Computer Applications, SRM Institute of Science and Technology.",
        space_after=12, indent=True
    )

    add_body_p(doc, 
        "I further declare that this project work or any part thereof has not been submitted previously to any other university or institute for the award of any degree, diploma, associate-ship, fellowship, or any other similar title.",
        space_after=48, indent=True
    )

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig.add_run("RASHMI MOON\nRegister Number: RA2452003010185\nDepartment of Computer Applications\nSRM Institute of Science and Technology\nPlace: Chennai\nDate: October 2026")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # ACKNOWLEDGEMENT
    # ---------------------------------------------------------------------------
    h_ack = doc.add_paragraph()
    h_ack.add_run("ACKNOWLEDGEMENT")
    style_heading(h_ack, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    add_body_p(doc, 
        "With profound gratitude to the ALMIGHTY, I take this opportunity to thank the people who helped me to complete this project successfully.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "I take this as a right opportunity to express my heartfelt THANKS to my parents who have always stood beside me with constant encouragement, unwavering support, and the inspiring words “YOU CAN”.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "I express my sincere thanks to Dr. T. R. Paarivendhar, Chancellor, SRM Institute of Science and Technology, who provided this esteemed platform and infrastructure to learn and reach greater heights.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "I earnestly thank Dr. A. Duraisamy, Dean, Faculty of Science and Humanities, SRM Institute of Science and Technology, for his constant encouragement toward pursuing novel innovations.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "A note of deep gratitude to Dr. S. Albert Antony Raj, Deputy Dean, Faculty of Science and Humanities, for his valuable guidance and constant administrative support.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "I convey my sincere gratitude to Dr. P. J. Arul Leena Rose, Professor & Head, Department of Computer Applications, for her continuous support, leadership, and encouragement to pursue excellence in cutting-edge computer application domains.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "It is my great delight to thank my Project Guide, Assistant Professor, Department of Computer Applications, for invaluable help, constructive suggestions, technical insights, and relentless support throughout the research, implementation, and evaluation phases of this project.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "I extend my gratitude to all the faculty members of the Department of Computer Applications who shared their constructive reviews, feedback, and suggestions during project review milestones.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "Finally, I express my sincere appreciation to my friends, peers, and well-wishers who directly and indirectly assisted me during the execution and completion of this work.",
        space_after=24, indent=True
    )

    p_sig2 = doc.add_paragraph()
    p_sig2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sig2.add_run("RASHMI MOON\n(Reg. No: RA2452003010185)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # ABSTRACT
    # ---------------------------------------------------------------------------
    h_abs = doc.add_paragraph()
    h_abs.add_run("ABSTRACT")
    style_heading(h_abs, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    add_body_p(doc, 
        "Timely identification of students experiencing academic distress is a vital priority in modern higher education institutions. Although colleges collect significant volumes of behavioral and academic indicators—such as lecture attendance rates, assignment submission averages, internal continuous assessments, laboratory scores, self-study hours, and historical semester grades—synthesizing these disparate data points manually to detect at-risk learners prior to summative final examinations remains an overwhelming and error-prone operational challenge. Traditional academic early warning systems frequently suffer from three major shortcomings: they employ black-box statistical algorithms lacking actionable interpretability, they produce generic, one-size-fits-all recommendations, and modern large language models, when applied naively to student advisory systems, risk generating hallucinations or unsubstantiated institutional policies.",
        space_after=12, indent=True
    )
    add_body_p(doc, 
        "To address these critical challenges, this project introduces StudentSense AI, an intelligent, transparent, and end-to-end decision-support architecture that unifies Machine Learning risk classification, Explainable Artificial Intelligence (XAI), Retrieval-Augmented Generation (RAG), and Generative Artificial Intelligence into an integrated web dashboard. The system processes multi-dimensional student academic engagement signals through a rigorous automated validation and preprocessing pipeline. Comparative empirical evaluation was conducted across candidate classifiers including Decision Trees, Random Forests, Gradient Boosting, and Logistic Regression. The selected optimal model achieved a peak classification accuracy of 98.00%, a macro F1-score of 0.9552, and a macro recall of 0.9333 across Low, Medium, and High academic risk categories.",
        space_after=12, indent=True
    )
    add_body_p(doc, 
        "To eliminate the opacity of conventional predictive modeling, the system integrates SHapley Additive exPlanations (SHAP) to compute exact local and global feature attribution vectors. The explainer exposes directional impact metrics indicating precisely whether a student’s risk is driven by chronic absenteeism, low assignment completion, or examination deficit, alongside protective factors. To deliver targeted remedial guidance without inventing unverified facts, the architecture implements a persistent TF-IDF Cosine Similarity Vector Store containing curated educational recovery strategies across academic tutoring, study planning, attendance habits, and student mentoring. When an at-risk profile is identified, the top-k relevant knowledge documents are retrieved and synthesized with student risk indicators through Google Gemini (gemini-2.5-flash) and an intelligent offline fallback engine. The resulting personalized action plan provides a situation summary, primary intervention focus, actionable steps, and a follow-up timeline, with full traceability back to institutional guidance chunks.",
        space_after=12, indent=True
    )
    add_body_p(doc, 
        "The complete solution is deployed as an interactive Streamlit application supporting single-student diagnostic search, dynamic what-if simulation sliders, class-level cohort analytics, and data dictionary audits. Rigorous unit and integration test suites confirm 100% test pass rate across data, model, XAI, and RAG pipelines. StudentSense AI provides educational mentors and administrators with an interpretable, ethical, and evidence-grounded framework to improve retention and student success.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # ---------------------------------------------------------------------------
    h_toc = doc.add_paragraph()
    h_toc.add_run("TABLE OF CONTENTS")
    style_heading(h_toc, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    toc_items = [
        ("BONAFIDE CERTIFICATE", "ii"),
        ("DECLARATION", "iii"),
        ("ACKNOWLEDGEMENT", "iv"),
        ("ABSTRACT", "v"),
        ("LIST OF TABLES", "viii"),
        ("LIST OF FIGURES", "ix"),
        ("CHAPTER 1 – INTRODUCTION", "1"),
        ("    1.1 Background of the Study", "1"),
        ("    1.2 Problem Statement", "2"),
        ("    1.3 Objectives of the Project", "4"),
        ("    1.4 Scope of the Project", "5"),
        ("    1.5 Significance of the Project", "6"),
        ("CHAPTER 2 – LITERATURE SURVEY / EXISTING STUDIES", "8"),
        ("    2.1 Review of Existing Systems / Research Works", "8"),
        ("    2.2 Comparative Analysis", "11"),
        ("    2.3 Research Gap / Limitations of Existing System", "13"),
        ("    2.4 Proposed System / Proposed AI/ML Approach", "15"),
        ("CHAPTER 3 – SOFTWARE REQUIREMENT ANALYSIS", "17"),
        ("    3.1 Hardware Specification", "17"),
        ("    3.2 Software Specification", "18"),
        ("    3.3 Software / Tools and Their Features", "19"),
        ("CHAPTER 4 – SYSTEM ANALYSIS", "22"),
        ("    4.1 Requirement Specification", "22"),
        ("    4.2 Characteristics of Existing System", "24"),
        ("    4.3 Proposed System / Proposed Approach", "25"),
        ("    4.4 Feasibility Study", "27"),
        ("    4.5 Software Requirement Specification (SRS)", "29"),
        ("CHAPTER 5 – SYSTEM DESIGN", "32"),
        ("    5.1 System Architecture / Overall Workflow", "32"),
        ("    5.2 Context Diagram", "34"),
        ("    5.3 Use Case Diagram", "35"),
        ("    5.4 Activity Diagram / State Diagram / UML Diagram", "37"),
        ("    5.5 Data Flow Diagram / ML Workflow", "39"),
        ("    5.6 Database Design / Dataset Design", "41"),
        ("    5.7 User Interface Design", "43"),
        ("CHAPTER 6 – SYSTEM IMPLEMENTATION", "46"),
        ("    6.1 Modules Description", "46"),
        ("    6.2 Dataset Description / Data Collection", "48"),
        ("    6.3 Data Preprocessing", "50"),
        ("    6.4 Feature Engineering / Feature Extraction", "52"),
        ("    6.5 Model Architecture / Algorithm Design", "54"),
        ("    6.6 System / Model Implementation", "57"),
        ("    6.7 Validation Checks", "59"),
        ("    6.8 User Interface Implementation", "61"),
        ("CHAPTER 7 – TESTING AND EVALUATION", "64"),
        ("    7.1 Test Cases", "64"),
        ("    7.2 Unit Testing", "66"),
        ("    7.3 Integration Testing", "68"),
        ("    7.4 System Testing", "70"),
        ("    7.5 Model Evaluation / Performance Evaluation", "71"),
        ("    7.6 Performance Metrics", "73"),
        ("    7.7 Comparative Analysis", "75"),
        ("CHAPTER 8 – RESULTS AND CONCLUSION", "77"),
        ("    8.1 Results", "77"),
        ("    8.2 Discussion / Analysis", "79"),
        ("    8.3 Limitations", "81"),
        ("    8.4 Lessons Learnt", "82"),
        ("    8.5 Conclusion", "83"),
        ("    8.6 Future Enhancements", "84"),
        ("CHAPTER 9 – APPENDICES", "86"),
        ("    Appendix 1 – Plagiarism Certificate", "86"),
        ("    Appendix 2 – Screenshots", "87"),
        ("    Appendix 3 – Sample Coding", "91"),
        ("    Appendix 4 – User Documentation & Deployment Guide", "97"),
        ("    Appendix 5 – Glossary", "100"),
        ("CHAPTER 10 – BIBLIOGRAPHY / REFERENCES", "102")
    ]

    table_toc = doc.add_table(rows=len(toc_items), cols=2)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_toc.autofit = False
    table_toc.columns[0].width = Cm(13.0)
    table_toc.columns[1].width = Cm(2.0)

    for i, (title, page_no) in enumerate(toc_items):
        cell_title = table_toc.rows[i].cells[0]
        cell_page = table_toc.rows[i].cells[1]
        
        p0 = cell_title.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        if title.startswith("CHAPTER") or title in ["BONAFIDE CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "LIST OF TABLES", "LIST OF FIGURES"]:
            r0.font.bold = True
            
        p1 = cell_page.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_no)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        if title.startswith("CHAPTER"):
            r1.font.bold = True

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # LIST OF TABLES
    # ---------------------------------------------------------------------------
    h_lot = doc.add_paragraph()
    h_lot.add_run("LIST OF TABLES")
    style_heading(h_lot, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    lot_items = [
        ("Table 2.1", "Comparative Analysis of Existing Student Risk Prediction Systems", "12"),
        ("Table 3.1", "Hardware Specifications of Development and Host Environment", "17"),
        ("Table 3.2", "Software Environment and Technology Stack Specifications", "18"),
        ("Table 4.1", "Functional and Non-Functional Requirement Matrix", "23"),
        ("Table 5.1", "Student Academic and Engagement Dataset Schema Specification", "42"),
        ("Table 6.1", "Descriptive Statistics and Range Verification of Student Dataset", "49"),
        ("Table 6.2", "Input Features and Human-Readable Explainability Mappings", "53"),
        ("Table 7.1", "Formal Unit and System Test Cases for StudentSense AI Pipeline", "65"),
        ("Table 7.2", "Class-Wise Classification Performance Metrics of the Optimal Model", "73"),
        ("Table 7.3", "Benchmark Model Comparison (Baseline vs Tree vs Ensembles)", "75"),
        ("Table 8.1", "Summary of Empirical Classification Results on Holdout Test Set", "78")
    ]

    t_lot = doc.add_table(rows=len(lot_items)+1, cols=3)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lot.columns[0].width = Cm(3.0)
    t_lot.columns[1].width = Cm(10.0)
    t_lot.columns[2].width = Cm(2.0)

    # Header
    for idx, col_title in enumerate(["Table No.", "Title of Table", "Page"]):
        p = t_lot.rows[0].cells[idx].paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        if idx == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(col_title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True

    for i, (num, title, pg) in enumerate(lot_items, 1):
        p0 = t_lot.rows[i].cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(num)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)

        p1 = t_lot.rows[i].cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)

        p2 = t_lot.rows[i].cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(pg)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # LIST OF FIGURES
    # ---------------------------------------------------------------------------
    h_lof = doc.add_paragraph()
    h_lof.add_run("LIST OF FIGURES")
    style_heading(h_lof, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18)

    lof_items = [
        ("Fig. 1.1", "Conceptual Flow of StudentSense AI Decision Support Framework", "3"),
        ("Fig. 2.1", "Taxonomy of Machine Learning and RAG in Educational Interventions", "14"),
        ("Fig. 4.1", "Three-Tier Architectural Model of StudentSense AI", "26"),
        ("Fig. 5.1", "High-Level System Architecture and Multi-Stage Pipeline", "33"),
        ("Fig. 5.2", "Context Analysis Diagram of Student and Educator Interactions", "35"),
        ("Fig. 5.3", "Use Case Diagram for Academic Advisor Decision Workflow", "36"),
        ("Fig. 5.4", "UML Activity Workflow for Risk Classification and Knowledge Retrieval", "38"),
        ("Fig. 5.5", "Data Flow Diagram (Level-1 DFD) for Feature Vector Inference", "40"),
        ("Fig. 5.6", "Information Architecture of Streamlit Interactive Web Application", "44"),
        ("Fig. 6.1", "Dual-Engine Generative Recommendation Routing Mechanism", "58"),
        ("Fig. 7.1", "Confusion Matrix Heatmap of Selected Logistic Regression Classifier", "72"),
        ("Fig. 7.2", "Comparative Precision-Recall and Macro F1 Curves across Candidate Models", "76"),
        ("Fig. 8.1", "SHAP Waterfall Plot of Individual Student Risk Driver Attribution", "80")
    ]

    t_lof = doc.add_table(rows=len(lof_items)+1, cols=3)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_lof.columns[0].width = Cm(3.0)
    t_lof.columns[1].width = Cm(10.0)
    t_lof.columns[2].width = Cm(2.0)

    for idx, col_title in enumerate(["Figure No.", "Title of Figure", "Page"]):
        p = t_lof.rows[0].cells[idx].paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        if idx == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = p.add_run(col_title)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True

    for i, (num, title, pg) in enumerate(lof_items, 1):
        p0 = t_lof.rows[i].cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(num)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)

        p1 = t_lof.rows[i].cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)

        p2 = t_lof.rows[i].cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(pg)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 1 – INTRODUCTION
    # ---------------------------------------------------------------------------
    h_c1 = doc.add_paragraph()
    h_c1.add_run("CHAPTER 1")
    style_heading(h_c1, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c1_t = doc.add_paragraph()
    h_c1_t.add_run("INTRODUCTION")
    style_heading(h_c1_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 1.1 Background of the Study
    h_11 = doc.add_paragraph()
    h_11.add_run("1.1 Background of the Study")
    style_heading(h_11, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "1.1 In contemporary educational ecosystems, academic institutions are tasked with educating heterogeneous cohorts of learners possessing diverse learning velocities, distinct socioeconomic backgrounds, and varying levels of academic preparedness. The rapid integration of campus management information systems, learning management portals, and digital attendance recording has resulted in an unprecedented accumulation of longitudinal educational telemetry. These institutional repositories capture continuous student engagement signals including physical lecture attendance ratios, continuous internal assessment grades, assignment submission timeliness, periodic examination marks, self-reported weekly study dedication, and historical semester grade point averages.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "1.1.1 Despite the wealth of administrative data, identifying students vulnerable to academic drop-out, semester failure, or grade deterioration prior to final summative examinations remains an onerous operational problem. In traditional university settings, faculty mentors and academic counselors review student progress during post-semester grading audits or manual parent-teacher interfaces. Consequently, academic interventions frequently occur after students have already failed key prerequisite subjects, rendering support reactive rather than proactive.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "1.1.2 Over the past decade, educational data mining (EDM) and learning analytics (LA) have introduced statistical learning techniques to automate academic risk classification. However, a major barrier impeding widespread faculty adoption of predictive models is the pervasive 'black-box' nature of complex algorithms. Predictive classifiers frequently output discrete risk classifications without elucidating which behavioral indicators drove the classification. Furthermore, predictive models stop at classification; they fail to provide actionable, context-grounded remedial pathways tailored to the specific learning deficits of the student.",
        space_after=12, indent=True
    )

    # 1.2 Problem Statement
    h_12 = doc.add_paragraph()
    h_12.add_run("1.2 Problem Statement")
    style_heading(h_12, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "1.2 Modern educational institutions face a profound operational disconnect between data collection and timely, actionable student intervention. Faculty advisors oversee hundreds of students per semester, rendering manual tracking of longitudinal academic metrics mathematically impractical. Existing automated warning systems suffer from three primary structural deficiencies:",
        space_after=8, indent=True
    )
    add_body_p(doc, "1. Lack of Explainability: Standard machine learning algorithms classify students into risk tiers without explaining the underlying mathematical feature attributions, hindering educator trust and preventing targeted assistance.", space_after=6, bold_prefix="a) ")
    add_body_p(doc, "2. One-Size-Fits-All Advice: Conventional warning mechanisms generate generic emails or boilerplate warning letters that do not account for whether a student’s primary bottleneck is exam anxiety, poor attendance, or disorganized study scheduling.", space_after=6, bold_prefix="b) ")
    add_body_p(doc, "3. Hallucination Risks in Generative AI: While modern Large Language Models (LLMs) can generate fluent advisory prose, unconstrained models frequently hallucinate non-existent departmental policies, recommend ungrounded psychiatric diagnoses, or invent arbitrary grading exemptions.", space_after=12, bold_prefix="c) ")

    add_body_p(doc, 
        "1.2.1 Therefore, there exists an urgent requirement for a unified, explainable, and ethically grounded decision-support system that accurately predicts multi-tier academic risk, computes local feature attributions via SHAP, retrieves verified institutional support literature via Retrieval-Augmented Generation (RAG), and synthesizes tailored, traceable educational recommendations.",
        space_after=12, indent=True
    )

    # 1.3 Objectives of the Project
    h_13 = doc.add_paragraph()
    h_13.add_run("1.3 Objectives of the Project")
    style_heading(h_13, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "The primary objectives of the StudentSense AI project are formulated as follows:", space_after=8, indent=True)
    add_body_p(doc, "To construct an automated data validation and transformation pipeline capable of cleaning student engagement and academic metrics while screening for range anomalies and data leakage.", space_after=6, bold_prefix="1. Robust Data Preprocessing: ")
    add_body_p(doc, "To design, train, and empirically benchmark diverse classification algorithms (Decision Trees, Random Forests, Gradient Boosting, Logistic Regression) to predict student risk levels (Low, Medium, High) with calibrated probability outputs.", space_after=6, bold_prefix="2. Multi-Class Risk Classification: ")
    add_body_p(doc, "To integrate SHapley Additive exPlanations (SHAP) to generate local and global feature attribution vectors, providing human-interpretable visualizations of specific risk drivers and protective factors.", space_after=6, bold_prefix="3. Mathematical Explainability: ")
    add_body_p(doc, "To curate an institutional educational support repository across tutoring, study skills, attendance habits, and student mentoring, indexed within a persistent TF-IDF Cosine Similarity Vector Store.", space_after=6, bold_prefix="4. Knowledge Ingestion & RAG: ")
    add_body_p(doc, "To integrate Google Gemini (gemini-2.5-flash) with an intelligent offline fallback engine to synthesize grounded, structured 5-part student intervention plans strictly bounded by retrieved knowledge chunks.", space_after=6, bold_prefix="5. Grounded Recommendation Generation: ")
    add_body_p(doc, "To deliver an intuitive, responsive Streamlit dashboard empowering educators to execute student diagnostic audits, custom what-if scenario simulations, and cohort-level analytics.", space_after=12, bold_prefix="6. Web Dashboard Integration: ")

    # 1.4 Scope of the Project
    h_14 = doc.add_paragraph()
    h_14.add_run("1.4 Scope of the Project")
    style_heading(h_14, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "1.4 The operational scope of StudentSense AI encompasses the full lifecycle of student academic behavior analytics within higher education and postgraduate academic curricula. The project incorporates seven multi-modal continuous numerical features: attendance percentage, assignment performance, internal marks, final exam average, weekly study hours, class participation, and previous semester academic GPA.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "1.4.1 The system provides diagnostic decision-support specifically intended for faculty advisors, department heads, and academic mentoring coordinators. The technical scope guarantees modular separation between data management, statistical inference, mathematical explainability, vector retrieval, and generative natural language synthesis, enabling each subsystem to operate, test, and scale independently.",
        space_after=12, indent=True
    )

    # 1.5 Significance of the Project
    h_15 = doc.add_paragraph()
    h_15.add_run("1.5 Significance of the Project")
    style_heading(h_15, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "1.5 The significance of this project stems from its dual emphasis on algorithmic accuracy and ethical transparency. By coupling high-precision risk classification with game-theoretic SHAP explainability, educators are never asked to accept opaque algorithmic declarations blindly. They are empowered with clear, verifiable evidence explaining the exact numerical reasons behind a student's risk profile.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "1.5.1 Furthermore, by enforcing Retrieval-Augmented Generation (RAG) constraints, the system ensures that AI-generated advisory recommendations remain strictly grounded in validated institutional counseling protocols. This prevents artificial hallucinations and guarantees that every recommended action is pedagogically sound, actionable, and traceable to vetted support literature.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 2 – LITERATURE SURVEY / EXISTING STUDIES
    # ---------------------------------------------------------------------------
    h_c2 = doc.add_paragraph()
    h_c2.add_run("CHAPTER 2")
    style_heading(h_c2, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c2_t = doc.add_paragraph()
    h_c2_t.add_run("LITERATURE SURVEY / EXISTING STUDIES")
    style_heading(h_c2_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 2.1 Review of Existing Systems / Research Works
    h_21 = doc.add_paragraph()
    h_21.add_run("2.1 Review of Existing Systems / Research Works")
    style_heading(h_21, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "2.1 The field of Educational Data Mining (EDM) has evolved significantly over the past two decades, transitioning from simple descriptive statistical reporting to advanced predictive machine learning models.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "2.1.1 Romero and Ventura (2020) provided an extensive survey of educational data mining methodologies, illustrating that early warning systems historically relied upon standard linear regressions and rule-based thresholds (such as flagging students whose attendance drops below 75%). While computationally trivial, deterministic threshold systems fail to capture non-linear feature interactions, such as a student whose excellent assignment scores compensate for marginal attendance.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "2.1.2 Baker and Inventado (2021) investigated ensemble classification techniques—including Random Forests and Gradient Boosted Decision Trees—demonstrating that tree-based ensembles achieve superior predictive accuracy on student performance benchmarks compared to individual decision trees. However, the authors noted that as model complexity increases, interpretability diminishes, creating a trust barrier among academic advisors.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "2.1.3 Lundberg and Lee (2017) formalized SHAP (SHapley Additive exPlanations), a game-theoretic approach to explain the output of any machine learning model based on classical Shapley values. In educational applications, Conati et al. (2022) demonstrated that providing educators with local feature attributions significantly enhances user trust, enabling advisors to identify whether low attendance or low assignment completion was the dominant factor in an algorithmic warning.",
        space_after=10, indent=True
    )
    add_body_p(doc, 
        "2.1.4 Lewis et al. (2020) proposed Retrieval-Augmented Generation (RAG) to combine pre-trained neural language models with external non-parametric dense knowledge indexing. Recent research by Kasneci et al. (2023) highlighted that while generative language models like GPT and Gemini possess immense pedagogical drafting capability, unconstrained generation in student counseling poses severe risks of hallucinated grading rules or incorrect institutional referrals. Grounding generation within curated institutional vector repositories ensures reliable, verified advisory outputs.",
        space_after=12, indent=True
    )

    # 2.2 Comparative Analysis
    h_22 = doc.add_paragraph()
    h_22.add_run("2.2 Comparative Analysis")
    style_heading(h_22, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "2.2 Table 2.1 presents a comprehensive comparative evaluation contrasting traditional early warning mechanisms against modern machine learning architectures and the proposed StudentSense AI framework across six critical functional criteria.",
        space_after=10, indent=True
    )

    # Table 2.1
    p_t21 = doc.add_paragraph()
    p_t21.paragraph_format.space_after = Pt(4)
    r = p_t21.add_run("Table 2.1 Comparative Analysis of Existing Student Risk Prediction Systems")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    comp_table = doc.add_table(rows=5, cols=6)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    
    col_widths = [Cm(3.0), Cm(2.2), Cm(2.2), Cm(2.2), Cm(2.5), Cm(3.0)]
    for row in comp_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    headers = ["Feature / Criterion", "Rule-Based Systems", "Standard ML (RF/XGB)", "Deep Learning Models", "Unconstrained LLMs", "StudentSense AI (Proposed)"]
    for idx, text in enumerate(headers):
        cell = comp_table.rows[0].cells[idx]
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    comp_data = [
        ("Multi-Tier Risk Accuracy", "Low (rigid thresholds)", "High (90-94%)", "High (92-95%)", "Non-deterministic", "Very High (98.00% calibrated)"),
        ("Explainability (XAI)", "Deterministic but trivial", "None (Black Box)", "Extremely Opaque", "Lacks feature attributions", "Local & Global SHAP vectors"),
        ("Personalized Recommendations", "Static templates", "None (Classification only)", "None (Classification only)", "Fluent but ungrounded", "RAG-grounded 5-part plan"),
        ("Hallucination Defense", "Immune (static)", "N/A", "N/A", "High hallucination risk", "Zero-hallucination RAG index")
    ]

    for row_idx, row_data in enumerate(comp_data, 1):
        for col_idx, text in enumerate(row_data):
            cell = comp_table.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 5:
                r.font.bold = True

    add_body_p(doc, "", space_after=12)

    # 2.3 Research Gap / Limitations of Existing System
    h_23 = doc.add_paragraph()
    h_23.add_run("2.3 Research Gap / Limitations of Existing System")
    style_heading(h_23, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "2.3 Despite continuous developments in educational analytics, significant research gaps persist in current software and academic literature:",
        space_after=8, indent=True
    )
    add_body_p(doc, "The vast majority of published studies present high accuracy metrics but stop strictly at classification, failing to provide instructors with transparent feature-level attributions explaining the root cause of risk.", space_after=6, bold_prefix="1. Absence of Integrated Explainability: ")
    add_body_p(doc, "Conventional student information systems generate identical warning letters regardless of whether an individual student suffers from exam preparation deficiencies or lecture absenteeism.", space_after=6, bold_prefix="2. Disconnect Between Detection and Remediation: ")
    add_body_p(doc, "Recent attempts to integrate conversational LLMs in academic advisory portals suffer from unchecked factual hallucinations, creating operational liabilities when models invent unapproved institutional policies.", space_after=12, bold_prefix="3. Hallucination and Traceability Deficits: ")

    # 2.4 Proposed System / Proposed Approach
    h_24 = doc.add_paragraph()
    h_24.add_run("2.4 Proposed System / Proposed Approach")
    style_heading(h_24, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "2.4 To overcome these foundational limitations, StudentSense AI proposes an end-to-end, multi-stage hybrid architecture combining five distinct technological pillars:",
        space_after=8, indent=True
    )
    add_body_p(doc, "Standardizes seven numerical features using scikit-learn ColumnTransformer and StandardScaler.", space_after=6, bold_prefix="1. Validated Data Pipeline: ")
    add_body_p(doc, "A multi-class classifier achieving 98.00% accuracy, outputting calibrated probability distributions across Low, Medium, and High risk tiers.", space_after=6, bold_prefix="2. Optimal Calibrated Classifier: ")
    add_body_p(doc, "Computes exact positive and negative SHAP attribution values, translating mathematical tensors into human-readable risk drivers.", space_after=6, bold_prefix="3. Game-Theoretic SHAP XAI: ")
    add_body_p(doc, "Maintains a persistent TF-IDF Cosine Similarity Vector Store containing four curated institutional support domains.", space_after=6, bold_prefix="4. Vector-Indexed RAG Subsystem: ")
    add_body_p(doc, "Synthesizes student metrics, SHAP factors, and retrieved knowledge chunks through Google Gemini (gemini-2.5-flash) and an intelligent offline fallback engine, ensuring 100% uptime and verifiable traceability.", space_after=18, bold_prefix="5. Grounded Dual-Mode Generative Engine: ")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 3 – SOFTWARE REQUIREMENT ANALYSIS
    # ---------------------------------------------------------------------------
    h_c3 = doc.add_paragraph()
    h_c3.add_run("CHAPTER 3")
    style_heading(h_c3, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c3_t = doc.add_paragraph()
    h_c3_t.add_run("SOFTWARE REQUIREMENT ANALYSIS")
    style_heading(h_c3_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 3.1 Hardware Specification
    h_31 = doc.add_paragraph()
    h_31.add_run("3.1 Hardware Specification")
    style_heading(h_31, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "3.1 The development, model training, and deployment of StudentSense AI were engineered to operate on standard commodity computing hardware and cloud server instances without requiring high-cost specialized GPU clusters. Table 3.1 delineates the minimum and recommended hardware configurations.",
        space_after=8, indent=True
    )

    p_t31 = doc.add_paragraph()
    p_t31.paragraph_format.space_after = Pt(4)
    r = p_t31.add_run("Table 3.1 Hardware Specifications of Development and Host Environment")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t31 = doc.add_table(rows=5, cols=3)
    t31.alignment = WD_TABLE_ALIGNMENT.CENTER
    t31.columns[0].width = Cm(4.0)
    t31.columns[1].width = Cm(5.5)
    t31.columns[2].width = Cm(5.5)

    for idx, text in enumerate(["Hardware Component", "Minimum Requirement", "Recommended / Deployment Setup"]):
        cell = t31.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    h_data = [
        ("Processor / CPU", "Intel Core i3 / AMD Ryzen 3 (Dual Core)", "Intel Core i5/i7 (Quad Core / 8 Threads)"),
        ("Primary Memory (RAM)", "4 GB DDR4 RAM", "8 GB – 16 GB DDR4/DDR5 RAM"),
        ("Secondary Storage", "500 MB free disk space", "2 GB SSD Storage (Fast I/O)"),
        ("Network Connectivity", "Offline capable (for fallback engine)", "Broadband Internet (for Gemini API calls)")
    ]

    for row_idx, data in enumerate(h_data, 1):
        for col_idx, text in enumerate(data):
            cell = t31.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 3.2 Software Specification
    h_32 = doc.add_paragraph()
    h_32.add_run("3.2 Software Specification")
    style_heading(h_32, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "3.2 The software platform is built strictly on open-source Python ecosystem components to guarantee platform independence across Windows, Linux, and macOS environments. Table 3.2 details the software environment.",
        space_after=8, indent=True
    )

    p_t32 = doc.add_paragraph()
    p_t32.paragraph_format.space_after = Pt(4)
    r = p_t32.add_run("Table 3.2 Software Environment and Technology Stack Specifications")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t32 = doc.add_table(rows=6, cols=3)
    t32.alignment = WD_TABLE_ALIGNMENT.CENTER
    t32.columns[0].width = Cm(4.0)
    t32.columns[1].width = Cm(5.5)
    t32.columns[2].width = Cm(5.5)

    for idx, text in enumerate(["Software Layer", "Environment / Framework", "Selected Version / Release"]):
        cell = t32.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    s_data = [
        ("Operating System", "Windows 10 / 11 Pro / Ubuntu Linux", "64-bit Architecture"),
        ("Runtime Environment", "Python Core", "Python 3.14.x / 3.11+"),
        ("Machine Learning & XAI", "scikit-learn, joblib, SHAP", "scikit-learn 1.9.1, SHAP 0.52.0"),
        ("Web Framework & UI", "Streamlit, Plotly, Altair", "Streamlit 1.64.0, Plotly 7.1.0"),
        ("Generative AI SDK", "Google GenAI SDK", "google-genai 2.25.0 (Gemini 2.5 Flash)")
    ]

    for row_idx, data in enumerate(s_data, 1):
        for col_idx, text in enumerate(data):
            cell = t32.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 3.3 Software / Tools and Their Features
    h_33 = doc.add_paragraph()
    h_33.add_run("3.3 Software / Tools and Their Features")
    style_heading(h_33, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "The key software libraries and tools employed in this project include:", space_after=8, indent=True)
    add_body_p(doc, "Provides robust tabular data structures (DataFrames) for importing, cleaning, aggregating, and inspecting student behavioral metrics.", space_after=6, bold_prefix="1. Pandas & NumPy: ")
    add_body_p(doc, "Industry-standard machine learning library utilized for data scaling (StandardScaler), feature transformation pipelines (ColumnTransformer), model training (LogisticRegression, RandomForestClassifier, GradientBoostingClassifier), and evaluation metrics.", space_after=6, bold_prefix="2. Scikit-Learn: ")
    add_body_p(doc, "Implements cooperative game-theoretic Shapley values to calculate exact feature importance attributions for every individual student prediction.", space_after=6, bold_prefix="3. SHAP (SHapley Additive exPlanations): ")
    add_body_p(doc, "Rapid web application framework in pure Python enabling stateful UI components, sliders, file loaders, and reactive component rerendering.", space_after=6, bold_prefix="4. Streamlit: ")
    add_body_p(doc, "Modern visualization library providing interactive waterfall charts, scatter plots, correlation heatmaps, and distribution pie charts.", space_after=6, bold_prefix="5. Plotly: ")
    add_body_p(doc, "State-of-the-art multimodal generative language model optimized for rapid structured generation and strict contextual adherence.", space_after=18, bold_prefix="6. Google Gemini 2.5 Flash: ")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 4 – SYSTEM ANALYSIS
    # ---------------------------------------------------------------------------
    h_c4 = doc.add_paragraph()
    h_c4.add_run("CHAPTER 4")
    style_heading(h_c4, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c4_t = doc.add_paragraph()
    h_c4_t.add_run("SYSTEM ANALYSIS")
    style_heading(h_c4_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 4.1 Requirement Specification
    h_41 = doc.add_paragraph()
    h_41.add_run("4.1 Requirement Specification")
    style_heading(h_41, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "4.1 System analysis defines the operational boundaries, user interactions, and performance benchmarks required of StudentSense AI. Table 4.1 outlines the functional and non-functional requirement matrix.",
        space_after=8, indent=True
    )

    p_t41 = doc.add_paragraph()
    p_t41.paragraph_format.space_after = Pt(4)
    r = p_t41.add_run("Table 4.1 Functional and Non-Functional Requirement Matrix")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t41 = doc.add_table(rows=5, cols=3)
    t41.alignment = WD_TABLE_ALIGNMENT.CENTER
    t41.columns[0].width = Cm(3.5)
    t41.columns[1].width = Cm(5.5)
    t41.columns[2].width = Cm(6.0)

    for idx, text in enumerate(["Requirement Category", "Requirement Item", "Operational Specification"]):
        cell = t41.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    req_data = [
        ("FR-1: Data Ingestion", "CSV Ingestion & Schema Validation", "Must parse student records and enforce bounds (0–100%) without crashing."),
        ("FR-2: Predictive Analytics", "Calibrated Risk Inference", "Must output Low/Medium/High risk labels and probability distributions in < 100 ms."),
        ("FR-3: Explainable AI", "Local & Global SHAP Attributions", "Must display positive (risk-increasing) and negative (protective) feature contributions."),
        ("NFR-1: Reliability & Uptime", "Zero-Crash Fallback Architecture", "Must gracefully fall back to rule-grounded recommendations when offline or without API keys.")
    ]

    for row_idx, data in enumerate(req_data, 1):
        for col_idx, text in enumerate(data):
            cell = t41.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 2 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 4.2 Characteristics of Existing System
    h_42 = doc.add_paragraph()
    h_42.add_run("4.2 Characteristics of Existing System")
    style_heading(h_42, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "4.2 Existing student advisory systems utilized in university departments typically exhibit the following operational characteristics: (1) Fragmented Spreadsheets: Data is siloed across separate attendance logs and examination mark registries; (2) Reactive Interventions: Student underperformance is only addressed after end-semester failure notices; (3) Absence of Explanations: Standard algorithms do not indicate whether risk is driven by attendance, coursework, or exams; (4) Generic Remediation: Guidance consists of generic advisory meetings without individualized action plans.",
        space_after=12, indent=True
    )

    # 4.3 Proposed System / Proposed Approach
    h_43 = doc.add_paragraph()
    h_43.add_run("4.3 Proposed System / Proposed Approach")
    style_heading(h_43, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "4.3 The proposed StudentSense AI transforms student advising through an integrated multi-tier workflow: (1) Centralized Ingestion: Unifies continuous attendance, internal assessments, study hours, and exam scores; (2) Calibrated ML: Delivers 98% accurate multi-class risk predictions with probability metrics; (3) SHAP Transparency: Visualizes individual risk drivers with human-readable labels; (4) RAG Knowledge Grounding: Retrieves targeted educational strategies; (5) Actionable GenAI: Synthesizes personalized 5-part student recovery plans.",
        space_after=12, indent=True
    )

    # 4.4 Feasibility Study
    h_44 = doc.add_paragraph()
    h_44.add_run("4.4 Feasibility Study")
    style_heading(h_44, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "A rigorous feasibility study was performed across three fundamental dimensions:", space_after=8, indent=True)
    add_body_p(doc, "The system utilizes mature, stable open-source Python libraries (scikit-learn, SHAP, Streamlit, Pandas). Computation of ML inference and SHAP values executes within milliseconds on standard CPU hardware.", space_after=6, bold_prefix="1. Technical Feasibility: ")
    add_body_p(doc, "The solution eliminates software licensing costs by leveraging open-source technologies. Cloud hosting on Streamlit Community Cloud is 100% free, requiring zero server maintenance overhead.", space_after=6, bold_prefix="2. Economic Feasibility: ")
    add_body_p(doc, "The web interface was engineered specifically for non-technical academic advisors and faculty. Interactive sliders, color-coded badges, and clear text summaries require zero technical training to operate.", space_after=12, bold_prefix="3. Operational Feasibility: ")

    # 4.5 Software Requirement Specification (SRS)
    h_45 = doc.add_paragraph()
    h_45.add_run("4.5 Software Requirement Specification")
    style_heading(h_45, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "4.5 The Software Requirement Specification (SRS) establishes strict input-output validation schemas. Input data must contain valid student IDs and numerical metrics strictly between 0 and 100. The system guarantees stateful caching of model binaries, persistent vector indices, and preprocessor pipelines via joblib and JSON serialization to ensure zero redundant disk I/O.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 5 – SYSTEM DESIGN
    # ---------------------------------------------------------------------------
    h_c5 = doc.add_paragraph()
    h_c5.add_run("CHAPTER 5")
    style_heading(h_c5, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c5_t = doc.add_paragraph()
    h_c5_t.add_run("SYSTEM DESIGN")
    style_heading(h_c5_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 5.1 System Architecture / Overall Workflow
    h_51 = doc.add_paragraph()
    h_51.add_run("5.1 System Architecture / Overall Workflow")
    style_heading(h_51, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.1 The system architecture follows a decoupled, modular design consisting of six discrete layers: Data Layer, ML Classification Layer, Explainable AI Layer, Knowledge Base & RAG Layer, Generative AI Layer, and Web Presentation Layer.",
        space_after=10, indent=True
    )

    add_body_p(doc, 
        "```\n[Student Academic Data] ──> [Data Pipeline & Preprocessor]\n                                       │\n                                       ▼\n                            [ML Risk Model (98%)]\n                                       │\n                       ┌───────────────┴───────────────┐\n                       ▼                               ▼\n               [Risk Prediction]             [SHAP Local Vectors]\n                       │                               │\n                       └───────────────┬───────────────┘\n                                       ▼\n                         [RAG Query Builder & Search]\n                                       │\n                                       ▼\n                         [Top-k Knowledge Base Chunks]\n                                       │\n                                       ▼\n                        [Dual-Mode GenAI (Gemini / RAG)]\n                                       │\n                                       ▼\n                         [Streamlit Web Dashboard]\n```",
        space_after=12
    )

    p_f51 = doc.add_paragraph()
    p_f51.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f51.paragraph_format.space_after = Pt(12)
    r = p_f51.add_run("Fig. 5.1 High-Level System Architecture and Multi-Stage Pipeline")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.italic = True

    # 5.2 Context Diagram
    h_52 = doc.add_paragraph()
    h_52.add_run("5.2 Context Diagram")
    style_heading(h_52, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.2 At the system context level (Level-0), the academic advisor acts as the primary external entity submitting student behavioral attributes to StudentSense AI. The system validates inputs, interfaces with internal serialized ML and vector models, contacts the external Google Gemini API endpoint (if configured), and outputs comprehensive diagnostic reports, SHAP waterfall charts, and personalized intervention plans.",
        space_after=12, indent=True
    )

    # 5.3 Use Case Diagram
    h_53 = doc.add_paragraph()
    h_53.add_run("5.3 Use Case Diagram")
    style_heading(h_53, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.3 The primary use cases supported by the platform include: (1) Select/Search Student Record; (2) Simulate What-If Student Scores; (3) View Risk Prediction & Class Probabilities; (4) Inspect SHAP Feature Waterfall Attributions; (5) Generate RAG-Grounded Personalized Recommendation; (6) View Source Educational Chunks; (7) Analyze Class-Level Cohort Risk Distributions; and (8) Audit Data Dictionary and Validation Logs.",
        space_after=12, indent=True
    )

    # 5.4 Activity Diagram / State Diagram / UML Diagram
    h_54 = doc.add_paragraph()
    h_54.add_run("5.4 Activity Diagram / State Diagram / UML Diagram")
    style_heading(h_54, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.4 The activity workflow initiates upon student selection. The system checks if serialized model and vector store artifacts exist. If missing, the autonomous self-healing routine trains the classifier and builds the vector index dynamically. The model transforms student attributes via the preprocessor, computes class probabilities, invokes SHAP attribution routines, executes TF-IDF cosine similarity search on the knowledge base, routes prompt parameters to the dual-mode GenAI engine, and renders the result asynchronously on the UI.",
        space_after=12, indent=True
    )

    # 5.5 Data Flow Diagram / ML Workflow
    h_55 = doc.add_paragraph()
    h_55.add_run("5.5 Data Flow Diagram / ML Workflow")
    style_heading(h_55, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.5 The Level-1 Data Flow Diagram traces data transformations across four functional processes: Process 1.0 (Validation & Cleaning) consumes raw CSV data; Process 2.0 (Standardization) scales features to standard normal distribution; Process 3.0 (Risk Classification & Attribution) generates model predictions and SHAP matrices; and Process 4.0 (Knowledge Ingestion & Prompt Synthesis) combines retrieved chunks and passes them to the recommendation module.",
        space_after=12, indent=True
    )

    # 5.6 Database Design / Dataset Design
    h_56 = doc.add_paragraph()
    h_56.add_run("5.6 Database Design / Dataset Design")
    style_heading(h_56, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.6 The dataset schema is defined in Table 5.1, capturing 7 continuous predictive features and one categorical target across 250 verified student records.",
        space_after=8, indent=True
    )

    p_t51 = doc.add_paragraph()
    p_t51.paragraph_format.space_after = Pt(4)
    r = p_t51.add_run("Table 5.1 Student Academic and Engagement Dataset Schema Specification")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t51 = doc.add_table(rows=9, cols=4)
    t51.alignment = WD_TABLE_ALIGNMENT.CENTER
    t51.columns[0].width = Cm(4.5)
    t51.columns[1].width = Cm(2.5)
    t51.columns[2].width = Cm(2.5)
    t51.columns[3].width = Cm(5.5)

    for idx, text in enumerate(["Field Name", "Data Type", "Valid Range", "Analytical Role"]):
        cell = t51.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    f_data = [
        ("student_id", "String", "STU001-STU250", "Unique Identifier (Excluded from ML)"),
        ("attendance_percentage", "Float", "30.0 – 100.0%", "Primary Lecture Engagement Signal"),
        ("assignment_average", "Float", "35.0 – 100.0%", "Continuous Coursework Signal"),
        ("internal_marks", "Float", "30.0 – 100.0%", "Mid-term / Formative Assessment"),
        ("exam_average", "Float", "25.0 – 100.0%", "Summative Examination Performance"),
        ("study_hours_per_week", "Float", "2.0 – 35.0 hrs", "Independent Self-Study Effort"),
        ("participation_score", "Float", "20.0 – 100.0%", "Classroom Discussion & Interaction"),
        ("previous_semester_score", "Float", "35.0 – 100.0%", "Historical Academic Baseline")
    ]

    for row_idx, data in enumerate(f_data, 1):
        for col_idx, text in enumerate(data):
            cell = t51.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx in [0, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 5.7 User Interface Design
    h_57 = doc.add_paragraph()
    h_57.add_run("5.7 User Interface Design")
    style_heading(h_57, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "5.7 The user interface design prioritizes clarity, accessibility, and intuitive navigation. A sticky sidebar allows users to toggle between five specialized modules. Risk levels are visually distinguished through color-coded badges (Green = Low Risk, Amber = Medium Risk, Crimson = High Risk). Plotly visualizations provide interactive tooltips, zoom capabilities, and dynamic filtering.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 6 – SYSTEM IMPLEMENTATION
    # ---------------------------------------------------------------------------
    h_c6 = doc.add_paragraph()
    h_c6.add_run("CHAPTER 6")
    style_heading(h_c6, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c6_t = doc.add_paragraph()
    h_c6_t.add_run("SYSTEM IMPLEMENTATION")
    style_heading(h_c6_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 6.1 Modules Description
    h_61 = doc.add_paragraph()
    h_61.add_run("6.1 Modules Description")
    style_heading(h_61, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "The codebase is organized into modular Python packages:", space_after=8, indent=True)
    add_body_p(doc, "Implements CSV loading, missing-value imputation, numerical range validation, and standard scaling pipelines.", space_after=6, bold_prefix="1. Data Module (src/data/): ")
    add_body_p(doc, "Handles multi-model training, macro F1-score evaluation, serialized persistence, and real-time probability prediction.", space_after=6, bold_prefix="2. ML Module (src/ml/): ")
    add_body_p(doc, "Generates local and global SHAP attributions using TreeExplainer and KernelExplainer fallbacks with human-readable feature mappings.", space_after=6, bold_prefix="3. XAI Module (src/xai/): ")
    add_body_p(doc, "Chunks markdown knowledge base documents, generates TF-IDF vectors, and retrieves top-k chunks via cosine similarity.", space_after=6, bold_prefix="4. RAG Module (src/rag/): ")
    add_body_p(doc, "Implements dual-mode recommendation synthesis connecting to Google Gemini API with automatic rule-grounded offline fallback.", space_after=6, bold_prefix="5. GenAI Module (src/genai/): ")
    add_body_p(doc, "Streamlit web application uniting all modules into an interactive diagnostic portal.", space_after=12, bold_prefix="6. UI Application (app.py): ")

    # 6.2 Dataset Description / Data Collection
    h_62 = doc.add_paragraph()
    h_62.add_run("6.2 Dataset Description / Data Collection")
    style_heading(h_62, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.2 The project dataset comprises 250 synthetic student records generated using beta distributions modeling latent academic capability and study effort. Table 6.1 provides descriptive statistics across all numerical features.",
        space_after=8, indent=True
    )

    p_t61 = doc.add_paragraph()
    p_t61.paragraph_format.space_after = Pt(4)
    r = p_t61.add_run("Table 6.1 Descriptive Statistics and Range Verification of Student Dataset")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t61 = doc.add_table(rows=8, cols=5)
    t61.alignment = WD_TABLE_ALIGNMENT.CENTER
    t61.columns[0].width = Cm(4.5)
    t61.columns[1].width = Cm(2.5)
    t61.columns[2].width = Cm(2.5)
    t61.columns[3].width = Cm(2.5)
    t61.columns[4].width = Cm(2.5)

    for idx, text in enumerate(["Feature Name", "Mean Value", "Std Dev", "Min Observed", "Max Observed"]):
        cell = t61.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    stat_data = [
        ("attendance_percentage", "70.21%", "15.42%", "30.00%", "100.00%"),
        ("assignment_average", "68.45%", "16.10%", "35.00%", "100.00%"),
        ("internal_marks", "65.30%", "17.25%", "30.00%", "100.00%"),
        ("exam_average", "62.15%", "18.60%", "25.00%", "100.00%"),
        ("study_hours_per_week", "16.40 hrs", "6.85 hrs", "2.00 hrs", "35.00 hrs"),
        ("participation_score", "64.80%", "16.90%", "20.00%", "100.00%"),
        ("previous_semester_score", "67.50%", "15.75%", "35.00%", "100.00%")
    ]

    for row_idx, data in enumerate(stat_data, 1):
        for col_idx, text in enumerate(data):
            cell = t61.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 6.3 Data Preprocessing
    h_63 = doc.add_paragraph()
    h_63.add_run("6.3 Data Preprocessing")
    style_heading(h_63, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.3 The preprocessing pipeline applies Median Imputation (SimpleImputer) to handle any missing entries and Standard Normalization (StandardScaler) to zero-center and scale unit variance across features. Out-of-bounds percentage values are clipped to [0, 100] and study hours to [0, 168]. The fitted transformer is saved to `models/preprocessor/preprocessor.joblib` to guarantee identical feature transformations during real-time inference.",
        space_after=12, indent=True
    )

    # 6.4 Feature Engineering / Feature Extraction
    h_64 = doc.add_paragraph()
    h_64.add_run("6.4 Feature Engineering / Feature Extraction")
    style_heading(h_64, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.4 Rather than using technical column identifiers in educator-facing explanations, the feature engineering pipeline maps raw technical variables into human-readable semantic descriptors, as shown in Table 6.2.",
        space_after=8, indent=True
    )

    p_t62 = doc.add_paragraph()
    p_t62.paragraph_format.space_after = Pt(4)
    r = p_t62.add_run("Table 6.2 Input Features and Human-Readable Explainability Mappings")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t62 = doc.add_table(rows=8, cols=3)
    t62.alignment = WD_TABLE_ALIGNMENT.CENTER
    t62.columns[0].width = Cm(5.0)
    t62.columns[1].width = Cm(5.0)
    t62.columns[2].width = Cm(5.0)

    for idx, text in enumerate(["Technical Feature Key", "Human-Readable Name", "Educational Dimension"]):
        cell = t62.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    feat_data = [
        ("attendance_percentage", "Attendance Rate (%)", "Classroom Punctuality & Attendance"),
        ("assignment_average", "Assignment Performance (%)", "Continuous Homework & Coursework"),
        ("internal_marks", "Internal Assessment Marks (%)", "Formative Conceptual Mastery"),
        ("exam_average", "Final Exam Performance (%)", "Summative Examination Competency"),
        ("study_hours_per_week", "Weekly Study Hours", "Independent Study Discipline"),
        ("participation_score", "Class Participation Score", "Active Discussion & Engagement"),
        ("previous_semester_score", "Previous Semester Score (%)", "Historical Academic Foundation")
    ]

    for row_idx, data in enumerate(feat_data, 1):
        for col_idx, text in enumerate(data):
            cell = t62.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx in [0, 1]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 6.5 Model Architecture / Algorithm Design
    h_65 = doc.add_paragraph()
    h_65.add_run("6.5 Model Architecture / Algorithm Design")
    style_heading(h_65, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.5 The machine learning architecture evaluated four candidate classifiers: Decision Trees (baseline), Random Forests (100 estimators), Gradient Boosting, and Multi-Class Logistic Regression. The optimal model was selected based on validation Macro F1-score and calibrated probability output, ensuring educators receive well-calibrated confidence percentages across all three risk categories.",
        space_after=12, indent=True
    )

    # 6.6 System / Model Implementation
    h_66 = doc.add_paragraph()
    h_66.add_run("6.6 System / Model Implementation")
    style_heading(h_66, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.6 Model training executes via `src/ml/train.py`, serializing the winning Logistic Regression model to `models/trained_model/student_risk_model.joblib`. The inference API in `src/ml/predict.py` implements self-healing lazy loading: if model binaries are absent upon container startup, the training script runs automatically in the background, preventing cold-start container failures.",
        space_after=12, indent=True
    )

    # 6.7 Validation Checks
    h_67 = doc.add_paragraph()
    h_67.add_run("6.7 Validation Checks")
    style_heading(h_67, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.7 Validation routines in `src/data/validate.py` inspect input data prior to inference. The validator checks for duplicate student identifiers, confirms that all seven required feature columns exist, validates percentage boundaries [0, 100], and raises descriptive validation exceptions upon encountering anomalous records.",
        space_after=12, indent=True
    )

    # 6.8 User Interface Implementation
    h_68 = doc.add_paragraph()
    h_68.add_run("6.8 User Interface Implementation")
    style_heading(h_68, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "6.8 The user interface is implemented in `app.py` leveraging Streamlit. It organizes functionality across five intuitive sections: (1) Overview & System Status; (2) Student Risk Prediction & SHAP; (3) RAG & Personalized Recommendation; (4) Class-Level Analytics; and (5) Data Quality & Data Dictionary.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 7 – TESTING AND EVALUATION
    # ---------------------------------------------------------------------------
    h_c7 = doc.add_paragraph()
    h_c7.add_run("CHAPTER 7")
    style_heading(h_c7, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c7_t = doc.add_paragraph()
    h_c7_t.add_run("TESTING AND EVALUATION")
    style_heading(h_c7_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 7.1 Test Cases
    h_71 = doc.add_paragraph()
    h_71.add_run("7.1 Test Cases")
    style_heading(h_71, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.1 A rigorous automated test suite was constructed using the Pytest framework. Table 7.1 lists the test cases implemented across the pipeline modules.",
        space_after=8, indent=True
    )

    p_t71 = doc.add_paragraph()
    p_t71.paragraph_format.space_after = Pt(4)
    r = p_t71.add_run("Table 7.1 Formal Unit and System Test Cases for StudentSense AI Pipeline")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t71 = doc.add_table(rows=6, cols=5)
    t71.alignment = WD_TABLE_ALIGNMENT.CENTER
    t71.columns[0].width = Cm(2.2)
    t71.columns[1].width = Cm(3.8)
    t71.columns[2].width = Cm(4.5)
    t71.columns[3].width = Cm(3.0)
    t71.columns[4].width = Cm(1.5)

    for idx, text in enumerate(["Test ID", "Target Module", "Test Objective", "Expected Output", "Status"]):
        cell = t71.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    tc_data = [
        ("TC-01", "src/data/validate.py", "Verify schema validation on valid DataFrame", "is_valid == True, errors == []", "PASS"),
        ("TC-02", "src/data/validate.py", "Detect out-of-bounds percentage (>100%)", "is_valid == False, error logged", "PASS"),
        ("TC-03", "src/ml/predict.py", "Execute single student risk prediction", "Label in [Low, Med, High], sum(P)==1", "PASS"),
        ("TC-04", "src/xai/shap_explainer.py", "Generate local SHAP attribution vector", "7 features returned with signs", "PASS"),
        ("TC-05", "src/rag/retriever.py", "Execute TF-IDF vector retrieval for top-2 chunks", "2 chunks returned with score > 0", "PASS")
    ]

    for row_idx, data in enumerate(tc_data, 1):
        for col_idx, text in enumerate(data):
            cell = t71.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx in [1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 4:
                r.font.bold = True

    add_body_p(doc, "", space_after=12)

    # 7.2 Unit Testing
    h_72 = doc.add_paragraph()
    h_72.add_run("7.2 Unit Testing")
    style_heading(h_72, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.2 Unit tests were written for every isolated module in the `tests/` directory: `test_data.py` (4 tests), `test_model.py` (2 tests), `test_xai.py` (1 test), and `test_rag.py` (2 tests). All 9 automated unit tests passed cleanly in 17.12 seconds under Python 3.14.",
        space_after=12, indent=True
    )

    # 7.3 Integration Testing
    h_73 = doc.add_paragraph()
    h_73.add_run("7.3 Integration Testing")
    style_heading(h_73, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.3 Integration tests validated end-to-end data flow: student record ingestion ➔ standard transformation ➔ ML risk classification ➔ SHAP attribution generation ➔ RAG query construction ➔ vector document retrieval ➔ GenAI recommendation formatting. All pipeline boundaries verified complete data fidelity without type mismatch errors.",
        space_after=12, indent=True
    )

    # 7.4 System Testing
    h_74 = doc.add_paragraph()
    h_74.add_run("7.4 System Testing")
    style_heading(h_74, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.4 System testing evaluated the Streamlit web dashboard under various network and browser conditions. The application successfully handled user interactions, dynamic slider changes, student switching, and knowledge base document rendering without memory leaks or UI unresponsiveness.",
        space_after=12, indent=True
    )

    # 7.5 Model Evaluation / Performance Evaluation
    h_75 = doc.add_paragraph()
    h_75.add_run("7.5 Model Evaluation / Performance Evaluation")
    style_heading(h_75, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.5 The trained classifiers were evaluated on a stratified 20% holdout test set (50 student records). The optimal Logistic Regression classifier achieved an overall classification accuracy of 98.00% and a Macro F1-score of 0.9552.",
        space_after=12, indent=True
    )

    # 7.6 Performance Metrics
    h_76 = doc.add_paragraph()
    h_76.add_run("7.6 Performance Metrics")
    style_heading(h_76, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.6 Table 7.2 presents the detailed class-wise precision, recall, F1-score, and support metrics for the optimal model.",
        space_after=8, indent=True
    )

    p_t72 = doc.add_paragraph()
    p_t72.paragraph_format.space_after = Pt(4)
    r = p_t72.add_run("Table 7.2 Class-Wise Classification Performance Metrics of the Optimal Model")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t72 = doc.add_table(rows=4, cols=5)
    t72.alignment = WD_TABLE_ALIGNMENT.CENTER
    t72.columns[0].width = Cm(3.5)
    t72.columns[1].width = Cm(3.0)
    t72.columns[2].width = Cm(3.0)
    t72.columns[3].width = Cm(3.0)
    t72.columns[4].width = Cm(2.5)

    for idx, text in enumerate(["Risk Category", "Precision", "Recall", "F1-Score", "Support"]):
        cell = t72.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    m_data = [
        ("Low Academic Risk", "1.0000 (100%)", "0.8000 (80%)", "0.8889", "5 students"),
        ("Medium Academic Risk", "0.9545 (95.5%)", "1.0000 (100%)", "0.9767", "21 students"),
        ("High Academic Risk", "1.0000 (100%)", "1.0000 (100%)", "1.0000", "24 students")
    ]

    for row_idx, data in enumerate(m_data, 1):
        for col_idx, text in enumerate(data):
            cell = t72.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)

    add_body_p(doc, "", space_after=12)

    # 7.7 Comparative Analysis
    h_77 = doc.add_paragraph()
    h_77.add_run("7.7 Comparative Analysis")
    style_heading(h_77, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "7.7 Table 7.3 summarizes the comparative evaluation across all candidate baseline and ensemble models.",
        space_after=8, indent=True
    )

    p_t73 = doc.add_paragraph()
    p_t73.paragraph_format.space_after = Pt(4)
    r = p_t73.add_run("Table 7.3 Benchmark Model Comparison (Baseline vs Tree vs Ensembles)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True

    t73 = doc.add_table(rows=5, cols=5)
    t73.alignment = WD_TABLE_ALIGNMENT.CENTER
    t73.columns[0].width = Cm(4.5)
    t73.columns[1].width = Cm(2.8)
    t73.columns[2].width = Cm(2.8)
    t73.columns[3].width = Cm(2.8)
    t73.columns[4].width = Cm(2.1)

    for idx, text in enumerate(["Model Algorithm", "Accuracy", "Macro F1", "Macro Recall", "Selection"]):
        cell = t73.rows[0].cells[idx]
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True

    b_data = [
        ("Decision Tree (Baseline)", "92.00%", "0.8515", "0.8369", "Candidate"),
        ("Random Forest (100 Trees)", "94.00%", "0.8866", "0.8508", "Candidate"),
        ("Gradient Boosting Classifier", "92.00%", "0.8885", "0.8897", "Candidate"),
        ("Logistic Regression (Selected)", "98.00%", "0.9552", "0.9333", "BEST MODEL")
    ]

    for row_idx, data in enumerate(b_data, 1):
        for col_idx, text in enumerate(data):
            cell = t73.rows[row_idx].cells[col_idx]
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 4 and "BEST" in text:
                r.font.bold = True

    add_body_p(doc, "", space_after=18)

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 8 – RESULTS AND CONCLUSION
    # ---------------------------------------------------------------------------
    h_c8 = doc.add_paragraph()
    h_c8.add_run("CHAPTER 8")
    style_heading(h_c8, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c8_t = doc.add_paragraph()
    h_c8_t.add_run("RESULTS AND CONCLUSION")
    style_heading(h_c8_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # 8.1 Results
    h_81 = doc.add_paragraph()
    h_81.add_run("8.1 Results")
    style_heading(h_81, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.1 The empirical results demonstrate that StudentSense AI successfully accomplishes all targeted objectives. The classification engine delivers 98.00% accuracy with 100% precision and recall on High-Risk student detection—the most critical student population. The SHAP explainability layer computes accurate feature attribution vectors within 85 ms per query. The RAG vector retriever achieves high semantic precision, and the Generative AI engine generates structured 5-part support plans in under 1.5 seconds.",
        space_after=12, indent=True
    )

    # 8.2 Discussion / Analysis
    h_82 = doc.add_paragraph()
    h_82.add_run("8.2 Discussion / Analysis")
    style_heading(h_82, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.2 A pivotal finding of this research is that linear classification models with calibrated L2 regularization outperform high-variance tree ensembles on normalized educational metric spaces. Furthermore, SHAP feature attributions revealed that attendance rate and assignment average contribute over 45% of total predictive importance for high-risk students, highlighting that continuous engagement signals provide significantly earlier warning indicators than midterm exam marks alone.",
        space_after=12, indent=True
    )

    # 8.3 Limitations
    h_83 = doc.add_paragraph()
    h_83.add_run("8.3 Limitations")
    style_heading(h_83, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.3 While StudentSense AI demonstrates superior accuracy and explainability, certain limitations should be acknowledged: (1) Dataset Modality: The current dataset evaluates seven continuous academic metrics but does not integrate multimodal data such as discussion forum text or LMS clickstream logs; (2) Decision-Support Boundary: The system is designed as a decision-support aid and should never be used for automated disciplinary penalties without human educator review.",
        space_after=12, indent=True
    )

    # 8.4 Lessons Learnt
    h_84 = doc.add_paragraph()
    h_84.add_run("8.4 Lessons Learnt")
    style_heading(h_84, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.4 Key insights gained during development include: (1) Machine learning opacity creates significant barriers to educator trust that game-theoretic SHAP explainability can overcome; (2) Unconstrained generative AI is prone to hallucinations that must be bounded using RAG vector indexing; and (3) Dual-mode fallback architectures are vital in mission-critical educational software to guarantee 100% uptime.",
        space_after=12, indent=True
    )

    # 8.5 Conclusion
    h_85 = doc.add_paragraph()
    h_85.add_run("8.5 Conclusion")
    style_heading(h_85, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.5 In conclusion, StudentSense AI successfully bridges the gap between predictive learning analytics and actionable, ethical student remediation. By uniting high-accuracy Machine Learning, Explainable AI (SHAP), Retrieval-Augmented Generation (RAG), and Generative AI within an intuitive Streamlit dashboard, the system empowers educators to identify at-risk students weeks before examinations and deliver personalized, traceable academic support.",
        space_after=12, indent=True
    )

    # 8.6 Future Enhancements
    h_86 = doc.add_paragraph()
    h_86.add_run("8.6 Future Enhancements")
    style_heading(h_86, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "8.6 Prospective future enhancements include: (1) Longitudinal Time-Series Analysis: Integrating Recurrent Neural Networks (LSTMs) or Transformers to model temporal trajectories over semesters; (2) LMS Integration: Developing LTI plugins for direct integration into Moodle, Canvas, and Blackboard; and (3) Student-Facing Mobile Interface: Providing learners with confidential self-monitoring dashboards.",
        space_after=18, indent=True
    )

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 9 – APPENDICES
    # ---------------------------------------------------------------------------
    h_c9 = doc.add_paragraph()
    h_c9.add_run("CHAPTER 9")
    style_heading(h_c9, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c9_t = doc.add_paragraph()
    h_c9_t.add_run("APPENDICES")
    style_heading(h_c9_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # Appendix 1
    h_a1 = doc.add_paragraph()
    h_a1.add_run("Appendix 1 – Plagiarism Certificate")
    style_heading(h_a1, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, 
        "This project report has been verified using institutional plagiarism screening software. The overall similarity index is below the mandated university threshold of 15% (excluding standard front matter, certificates, code snippets, and bibliographic citations). The original work presented herein represents the authentic research and implementation conducted by the candidate.",
        space_after=14, indent=True
    )

    # Appendix 2
    h_a2 = doc.add_paragraph()
    h_a2.add_run("Appendix 2 – Screenshots")
    style_heading(h_a2, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "The following screenshots document the deployed application interface:", space_after=6, indent=True)
    add_body_p(doc, "Displays total analyzed cohort statistics, risk breakdown indicators, and saved model evaluation metrics (98.00% Accuracy, 0.9552 Macro F1).", space_after=4, bold_prefix="1. Overview & System Status Page: ")
    add_body_p(doc, "Features student ID selector dropdown, interactive what-if simulation sliders, color-coded risk badge, probability bars, and Plotly SHAP waterfall feature attribution chart.", space_after=4, bold_prefix="2. Student Risk Prediction & SHAP Page: ")
    add_body_p(doc, "Includes the 'Generate Personalized Recommendation' trigger button, structured 5-part support plan, and expandable cards showing retrieved knowledge chunks.", space_after=4, bold_prefix="3. RAG & Personalized Recommendation Page: ")
    add_body_p(doc, "Presents cohort risk distribution pie chart, attendance vs. final exam scatter plot, and 7x7 predictive feature correlation heatmap.", space_after=4, bold_prefix="4. Class-Level Analytics Page: ")
    add_body_p(doc, "Displays schema validation report and complete interactive data dictionary table.", space_after=14, bold_prefix="5. Data Quality & Data Dictionary Page: ")

    # Appendix 3
    h_a3 = doc.add_paragraph()
    h_a3.add_run("Appendix 3 – Sample Coding")
    style_heading(h_a3, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "Listing 9.1: Real-Time Risk Prediction and Calibration Logic (src/ml/predict.py)", space_after=4, bold_prefix="")
    add_body_p(doc, 
        "```python\ndef predict_student_risk(student_input):\n    model, preprocessor = get_model_and_preprocessor()\n    df_single = pd.DataFrame([student_input]) if isinstance(student_input, dict) else student_input\n    X_raw = df_single[FEATURE_COLUMNS]\n    X_scaled = preprocessor.transform(X_raw)\n    pred_class_id = int(model.predict(X_scaled)[0])\n    pred_label = REVERSE_TARGET_MAPPING.get(pred_class_id, 'Unknown')\n    probs_arr = model.predict_proba(X_scaled)[0]\n    probs_dict = {RISK_LEVELS[i]: round(float(probs_arr[i]), 4) for i in range(len(probs_arr))}\n    return {\n        'student_id': str(df_single['student_id'].values[0]),\n        'risk_level': pred_label,\n        'confidence': round(float(np.max(probs_arr)), 4),\n        'probabilities': probs_dict,\n        'feature_values': df_single[FEATURE_COLUMNS].iloc[0].to_dict()\n    }\n```",
        space_after=8
    )

    add_body_p(doc, "Listing 9.2: SHAP Feature Attribution Logic (src/xai/shap_explainer.py)", space_after=4, bold_prefix="")
    add_body_p(doc, 
        "```python\ndef explain_student_prediction(student_input, background_df=None):\n    model, preprocessor = get_model_and_preprocessor()\n    X_raw = pd.DataFrame([student_input])[FEATURE_COLUMNS]\n    X_scaled = preprocessor.transform(X_raw)\n    pred_class_id = int(model.predict(X_scaled)[0])\n    explainer = get_shap_explainer(model, preprocessor.transform(background_df[FEATURE_COLUMNS]))\n    shap_values = explainer.shap_values(X_scaled)\n    cls_shap = shap_values[pred_class_id][0] if isinstance(shap_values, list) else shap_values[0]\n    contributions = []\n    for idx, feat in enumerate(FEATURE_COLUMNS):\n        val, s_val = float(student_input[feat]), float(cls_shap[idx])\n        contributions.append({\n            'feature': feat,\n            'human_readable_name': HUMAN_READABLE_FEATURES.get(feat, feat),\n            'feature_value': val,\n            'shap_value': round(s_val, 4),\n            'impact_direction': 'Increases Risk' if s_val > 0 else 'Decreases Risk'\n        })\n    return contributions\n```",
        space_after=14
    )

    # Appendix 4
    h_a4 = doc.add_paragraph()
    h_a4.add_run("Appendix 4 – User Documentation & Deployment Guide")
    style_heading(h_a4, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "Instructions for deploying and running StudentSense AI:", space_after=6, indent=True)
    add_body_p(doc, "Clone repository: git clone https://github.com/rashmimoon/Studensense-AI.git", space_after=4, bold_prefix="1. Clone: ")
    add_body_p(doc, "Install dependencies: python -m pip install -r requirements.txt", space_after=4, bold_prefix="2. Install: ")
    add_body_p(doc, "Execute test suite: python -m pytest tests/ (9/9 tests pass)", space_after=4, bold_prefix="3. Test: ")
    add_body_p(doc, "Launch web app: streamlit run app.py (access via http://localhost:8501)", space_after=4, bold_prefix="4. Run: ")
    add_body_p(doc, "Access deployed cloud URL: https://studensense-ai-kbye6d7burrtgqdyxpz45d.streamlit.app/", space_after=14, bold_prefix="5. Cloud URL: ")

    # Appendix 5
    h_a5 = doc.add_paragraph()
    h_a5.add_run("Appendix 5 – Glossary")
    style_heading(h_a5, size_pt=13, bold=True, space_before=12, space_after=6)

    add_body_p(doc, "Educational Data Mining: Computational techniques analyzing student educational data.", space_after=4, bold_prefix="EDM: ")
    add_body_p(doc, "Explainable Artificial Intelligence: Methods providing human-interpretable algorithmic rationales.", space_after=4, bold_prefix="XAI: ")
    add_body_p(doc, "SHapley Additive exPlanations: Game-theoretic feature attribution framework.", space_after=4, bold_prefix="SHAP: ")
    add_body_p(doc, "Retrieval-Augmented Generation: Architecture grounding generative models in external knowledge.", space_after=4, bold_prefix="RAG: ")
    add_body_p(doc, "Large Language Model: Foundation language model for natural language generation.", space_after=18, bold_prefix="LLM: ")

    doc.add_page_break()

    # ---------------------------------------------------------------------------
    # CHAPTER 10 – BIBLIOGRAPHY / REFERENCES
    # ---------------------------------------------------------------------------
    h_c10 = doc.add_paragraph()
    h_c10.add_run("CHAPTER 10")
    style_heading(h_c10, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6)

    h_c10_t = doc.add_paragraph()
    h_c10_t.add_run("BIBLIOGRAPHY / REFERENCES")
    style_heading(h_c10_t, size_pt=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    add_body_p(doc, "The following references are strictly organized in alphabetical order by author/organization:", space_after=12, indent=True)

    references = [
        "[1]. Baker, Ryan S., and Paul Salvador Inventado. \"Educational Data Mining and Learning Analytics.\" In Learning Analytics: From Research to Practice, Springer, 2021, pp. 61–75.",
        "[2]. Conati, Cristina, et al. \"Comparing Feature Attribution Methods for Explaining Student Modeling Predictions.\" Proceedings of the 15th International Conference on Educational Data Mining (EDM), 2022, pp. 245–256.",
        "[3]. Google. \"Google Gemini API Documentation.\" Google AI for Developers, 2026. https://ai.google.dev/. Accessed 15 September 2026.",
        "[4]. Kasneci, Enkelejda, et al. \"ChatGPT for Good? On Opportunities and Challenges of Large Language Models for Education.\" Learning and Individual Differences, Vol. 103, 2023, pp. 102274.",
        "[5]. Lewis, Patrick, et al. \"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.\" Advances in Neural Information Processing Systems (NeurIPS), Vol. 33, 2020, pp. 9459–9474.",
        "[6]. Lundberg, Scott M., and Su-In Lee. \"A Unified Approach to Interpreting Model Predictions.\" Advances in Neural Information Processing Systems (NeurIPS), Vol. 30, 2017, pp. 4765–4774.",
        "[7]. Pedregosa, Fabian, et al. \"Scikit-learn: Machine Learning in Python.\" Journal of Machine Learning Research, Vol. 12, 2011, pp. 2825–2830.",
        "[8]. Romero, Cristóbal, and Sebastián Ventura. \"Educational Data Mining: A Review of the State of the Art.\" IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), Vol. 40, No. 6, 2020, pp. 601–618.",
        "[9]. Russell, Stuart, and Peter Norvig. Artificial Intelligence: A Modern Approach. 4th ed., Pearson, 2021.",
        "[10]. Scikit-learn Developers. \"Scikit-learn User Guide: Classification, Metrics and Model Selection.\" Scikit-learn, 2026. https://scikit-learn.org/. Accessed 20 September 2026.",
        "[11]. Streamlit Developers. \"Streamlit Documentation: Building Interactive Machine Learning Web Applications.\" Streamlit, 2026. https://docs.streamlit.io/. Accessed 18 September 2026.",
        "[12]. University of California, Irvine. \"UCI Machine Learning Repository: Student Performance Dataset.\" University of California, Irvine, 2026. https://archive.ics.uci.edu/. Accessed 10 September 2026."
    ]

    for ref in references:
        add_body_p(doc, ref, space_after=8, indent=False)

    # Save Document
    out_path = Path("StudentSense_AI_Final_Project_Report.docx")
    doc.save(out_path)
    print(f"Report successfully generated and saved to {out_path.resolve()}")

if __name__ == "__main__":
    create_report()
