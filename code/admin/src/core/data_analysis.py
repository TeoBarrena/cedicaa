import pandas as pd
from src.core import jinete_amazonas as ja
from src.core import collection_record as cr
from src.core import employees
import locale

try:
    # Opcion anterior-> locale.setlocale(locale.LC_TIME, 'es_ES')
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    print("Locale es_ES.UTF-8 no está disponible, volviendo a la configuración predeterminada.")
    locale.setlocale(locale.LC_TIME, 'C')  # Configuración predeterminada

def get_riders_scholarship_data():
    """
    Retorna un DataFrame con la cantidad de becados y no becados.
    """
    data = ja.get_riders_scholarship_data()
    df = pd.DataFrame(data, columns=['scholarship', 'count'])
    df['scholarship'] = df['scholarship'].apply(lambda x: 'Becado' if x else 'No Becado')
    
    return df

def get_monthly_income(start_date, end_date):
    """
    Devuelve un DataFrame con los ingresos mensuales en un rango de fechas.
    """
    data = cr.get_between_dates(start_date, end_date)
    df = pd.DataFrame(data, columns=['year', 'month', 'monthly_income'])
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    df = df[['date', 'monthly_income']]

    return df


def get_riders_dishability_type_data():
    """
    Retorna un DataFrame con la cantidad de J&A por tipo de discapacidad.
    """
    data = ja.get_riders_dishability_type_data()
    data = process_data(data)
    df = pd.DataFrame(data, columns=['dishability_type', 'count'])

    return df

def process_data(data):
    """
    Procesa los datos de tipo de discapacidad porque un J&A puede tener más de uno.
    """
    processed_data = []
    for item in data:
        disability_types = item[0].split(', ')
        for disability in disability_types:
            processed_data.append((disability, item[1]))

    return processed_data

def get_riding_programs():
    """
    Retorna un DataFrame con las propuestas de trabajo de los Jinetes y Amazonas.
    """
    data = ja.get_riding_programs()
    df = pd.DataFrame(data, columns=['rider_type', 'count'])
    df.insert(0, 'ranking', ['#' + str(i+1) for i in range(len(df))])

    return df

def get_debtor_riders(page, per_page):
    """
    Retorna un DataFrame con los jinetes con deudas pendientes.
    """
    data = cr.get_debtor_riders(page, per_page)
    df = pd.DataFrame(data, columns=['first_name', 'last_name', 'total_due'])
    df['full_name'] = df['last_name'] + ', ' + df['first_name']

    return df

def get_professionals_work(page, per_page):
    """
    Retorna un DataFrame con la cantidad de profesionales que trabajan en el centro.
    """
    data = employees.work_count(page, per_page)
    df = pd.DataFrame(data, columns=["dni", "name_lastname", "count", "profession"])

    return df