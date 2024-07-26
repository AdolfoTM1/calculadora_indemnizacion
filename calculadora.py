import pandas as pd
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display, HTML

def calculate_indemnification(name, salary, start_date, end_date, vacation_debt_days):
    # Convertir las fechas
    start_date = datetime.strptime(start_date, '%d-%m-%Y')
    end_date = datetime.strptime(end_date, '%d-%m-%Y')

    # Cálculo de antigüedad en años
    years_worked = (end_date - start_date).days / 365.25
    years_worked_int = int(years_worked)

    # Cálculo de antigüedad (en días)
    seniority_days = (end_date - start_date).days

    # Cálculo de salario diario
    daily_salary = salary / 30

     # Cálculo de salario vacaciones
    vacation_salary = salary / 25

    # Cálculo de indemnización por despido (un sueldo por año o fracción mayor a tres meses)
    if (years_worked - years_worked_int) > 0.25:
        years_worked_int += 1
    indemnification = daily_salary * 30 * years_worked_int

    # Cálculo del preaviso (un mes de salario)
    notice_period = salary

    # Cálculo del SAC proporcional
    sac_proportional = (salary / 12) * (seniority_days / 365.25)

    # Cálculo de vacaciones proporcionales y SAC sobre vacaciones
    if years_worked_int < 5:
        vacation_days = 14
    elif years_worked_int < 10:
        vacation_days = 21
    elif years_worked_int < 20:
        vacation_days = 28
    else:
        vacation_days = 35

    vacation_proportional = vacation_salary * (vacation_days / 12)
    sac_vacation_proportional = vacation_proportional / 12

    # Cálculo del SAC sobre días trabajados
    worked_days = end_date.day
    sac_worked_days = (daily_salary * worked_days) / 12

    # Integración (días faltantes para terminar el mes)
    integration_days = 30 - (end_date.day % 30)
    integration = daily_salary * integration_days

    # Vacaciones no gozadas
    debt_vacation = vacation_salary * vacation_debt_days
    sac_debt_vacation = debt_vacation / 12

    # Resultados en formato vertical
    results = {
        'Indemnización por Despido': indemnification,
        'Preaviso': notice_period,
        'SAC sobre Preaviso': notice_period / 12,
        'Días Trabajados': daily_salary * end_date.day,
        'SAC sobre Días Trabajados': sac_worked_days,
        'SAC Proporcional': sac_proportional,
        'Vacaciones No Gozadas': debt_vacation,
        'SAC sobre Vacaciones No Gozadas': sac_debt_vacation,
        'Vacaciones Proporcionales': vacation_proportional,
        'SAC sobre Vacaciones Proporcionales': sac_vacation_proportional,
        'Integración': integration
    }

    total_liquidation = sum(results.values())

    # Convertir los resultados en DataFrame y transponer para mostrar en formato vertical
    result_df = pd.DataFrame.from_dict(results, orient='index', columns=['Monto'])
    result_df.loc['Total'] = total_liquidation
    return name, result_df, years_worked_int

# Widgets para la interfaz de Voila
name_input = widgets.Text(
    value='Nombre Apellido',
    description='Nombre:'
)

salary_input = widgets.FloatText(
    value=0.0,
    description='Salario:',
    step=0.01
)

start_date_input = widgets.Text(
    value='01-01-2020',
    description='Fecha Inicio (dd-mm-yyyy):'
)

end_date_input = widgets.Text(
    value='01-07-2024',
    description='Fecha Fin (dd-mm-yyyy):'
)

vacation_debt_days_input = widgets.IntText(
    value=0,
    description='Vacaciones Adeudadas (días):'
)

calculate_button = widgets.Button(
    description='Calcular',
    button_style='success'
)

output_area = widgets.Output()

def on_calculate_button_clicked(b):
    with output_area:
        output_area.clear_output()
        name, result, years_worked = calculate_indemnification(
            name_input.value,
            salary_input.value,
            start_date_input.value,
            end_date_input.value,
            vacation_debt_days_input.value
        )
        display(HTML(f"<b>Nombre: {name}</b>"))
        display(HTML(f"<b>Años Trabajados: {years_worked}</b>"))
        display(result)

calculate_button.on_click(on_calculate_button_clicked)

# Mostrar widgets
display(name_input, salary_input, start_date_input, end_date_input, vacation_debt_days_input, calculate_button, output_area)

