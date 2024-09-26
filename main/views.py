from django.shortcuts import render, redirect
from .services import get_all_rows, GSPREAD_CLIENT
from setup.static.data.laboratorios import LABORATORIOS
from datetime import datetime, timedelta


def reservation_form(request):
    context = {"laboratorios": LABORATORIOS}

    if request.method == "POST":
        laboratorio = request.POST.get("lab")
        data = request.POST.get("date")
        professor = request.POST.get("professor")
        disciplina = request.POST.get("discipline")
        materiais = request.POST.get("materials")

        # Converter a data recebida em formato datetime
        data_obj = datetime.strptime(data, "%Y-%m-%d")

        # Verificar se a data está dentro do prazo de 2 dias
        if data_obj < datetime.now() + timedelta(days=1):
            context["error"] = "Você deve reservar o laboratório com pelo menos 2 dias de antecedência."
        else:
            # Verificar se já existe uma reserva para o laboratório na mesma data
            reservations = get_all_rows("Test sheet")
            for reservation in reservations:
                if (
                    reservation["laboratorio"] == laboratorio
                    and reservation["data"] == data_obj
                ):
                    context["error"] = "Este laboratório já está reservado para essa data."
                    break
            else:
                # Se não houver conflito, adicionar a nova reserva
                sh = GSPREAD_CLIENT.open("Test sheet")
                worksheet = sh.get_worksheet(0)
                worksheet.append_row([laboratorio, data, professor, disciplina, materiais])
                context["success"] = "Reserva realizada com sucesso!"
                return redirect("reservation_form")

    reservations = get_all_rows("Test sheet")
    context["reservations"] = reservations

    # Coletar dados únicos para os filtros
    context["unique_labs"] = list(set(reservation["laboratorio"] for reservation in reservations))
    context["unique_professors"] = list(set(reservation["professor"] for reservation in reservations))
    context["unique_disciplines"] = list(set(reservation["disciplina"] for reservation in reservations))

    return render(request, "index.html", context)
