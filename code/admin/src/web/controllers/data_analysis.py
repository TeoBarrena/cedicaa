from flask import Blueprint, render_template, request
from src.core import data_analysis
import plotly.express as px
from datetime import date, datetime
from src.core import collection_record as cr
from src.core import employees 
from src.web.handlers.auth import check

bp = Blueprint("reports", __name__, url_prefix="/reportes")

@bp.route('/', methods=['GET'])
@check("data_analysis_index")
def index():
    """
    Mostrar menú de opciones para los reportes y gráficos.
    """
    return render_template('data_analysis/index.html')

@bp.route('/grafico-becados', methods=['GET'])
@check("data_analysis_show")
def grafico_becados():
    """
    Mostrar un gráfico de torta con la distribución de Jinetes y Amazonas Becados.
    """
    df = data_analysis.get_riders_scholarship_data()

    fig = px.pie(
        df,
        names='scholarship',
        values='count',
        title='Distribución de Jinetes y Amazonas Becados',
        hover_data={'scholarship': False, 'count': True} 
    )
    
    fig.update_traces(hovertemplate='%{label}: %{value}')

    fig.update_layout(legend_title="Estado de Beca")

    graph_html = fig.to_html(full_html=False)

    return render_template('data_analysis/grafico_becados.html', graph_html=graph_html)


@bp.route('/grafico-ingresos', methods=['GET', 'POST'])
@check("data_analysis_show")
def grafico_ingresos():
    """
    Muestra un gráfico de línea con la cantidad de ingresos por año o mes.
    """
    
    end_date = date.today()
    start_date = end_date.replace(year=end_date.year - 1)    
    
    if request.method == 'POST':
        start_date = request.form.get('start_date', start_date)
        end_date = request.form.get('end_date', end_date)
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    df = data_analysis.get_monthly_income(start_date, end_date)
    fig = px.line(df, x='date', y='monthly_income', title='Ingresos Mensuales', 
                    labels={'date': 'Fecha', 'monthly_income': 'Ingreso'})
    fig.update_xaxes(dtick="M1", tickformat="%b %Y")
    fig.update_yaxes(title_text="Ingreso", rangemode="tozero")
    graph_html = fig.to_html(full_html=False)
    
    return render_template('data_analysis/grafico_ingresos.html', graph_html=graph_html, start_date=start_date, 
                            end_date=end_date)


@bp.route('/grafico-tipo-discapacidad', methods=['GET'])
@check("data_analysis_show")
def grafico_tipos_discapacidad():
    """
    Mostrar un gráfico de torta con la distribución de Jinetes y Amazonas por tipo de discapacidad.
    """
    df = data_analysis.get_riders_dishability_type_data()

    fig = px.pie(
        df,
        names='dishability_type',
        values='count',
        title='Distribución de Jinetes y Amazonas por tipo de discapacidad',
        hover_data={'dishability_type': False, 'count': True} 
    )

    fig.update_traces(hovertemplate='%{label}: %{value}')
    fig.update_layout(legend_title="Tipo de discapacidad")
    graph_html = fig.to_html(full_html=False)

    return render_template('data_analysis/grafico_tipos_discapacidad.html', graph_html=graph_html)

@bp.route('/programas', methods=['GET'])
@check("data_analysis_show")
def get_programs_ranking():
    """
    Mostrar un reporte con el ranking de propuestas de trabajo de los Jinetes y Amazonas.
    """
    df = data_analysis.get_riding_programs()
    table_data = df.to_dict(orient='records')
    
    return render_template('data_analysis/reporte_programas.html', table_data=table_data)

@bp.route('/deudores', methods=['GET'])
@check("data_analysis_show")
def get_debtors_report():
    """
    Mostrar un reporte con los jinetes con deudas pendientes.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    debtors_pagination = cr.get_debtor_riders(page, per_page)
    df = data_analysis.get_debtor_riders(page, per_page)
    table_data = df.to_dict(orient='records')
    
    return render_template('data_analysis/reporte_deudores.html', table_data=table_data, page=page,
        per_page = per_page, debtors_pagination=debtors_pagination)

@bp.route('/carga-profesionales', methods=['GET'])
@check("data_analysis_show")
def get_professional_work():
    """
    Mostrar reporte de cantidad de trabajo asignado a los profesionales.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    professional_pagination = employees.work_count(page, per_page)
    df = data_analysis.get_professionals_work(page, per_page)
    table_data = df.to_dict(orient='records')

    return render_template('data_analysis/reporte_profesionales.html', table_data=table_data, page=page,
        per_page = per_page, professional_pagination=professional_pagination)