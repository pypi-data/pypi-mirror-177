#      Copyright (C)  2022. CQ Inversiones SAS.
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os
import uuid
from django.conf import settings
from django.utils import timezone
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Publication, Certificate

# Create your views here.


class GeneratePdf(View):
    """
    Clase que genera un PDF a partir de un template HTML
    """
    template_dir = "djangocms_zb_filer/"
    base_dir = "djangocms_zb_filer/certificates/"
    certificate_template = "certificate.html"

    def __get_template(self, template: object):
        template = self.template_dir + str(template) + "/" + self.certificate_template
        return template

    def __get_filepath(self, category: object):
        file_name = uuid.uuid4().hex + ".pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, self.base_dir + str(category))
        return file_path, file_name

    def __get_url(self, category: object, file_name: str):
        return settings.MEDIA_URL + self.base_dir + category + "/" + file_name

    def get(self, request, *args, **kwargs):
        """
        Responde a la petición GET vía HTTP
        :param request: request recibido vía HTTP
        :param args: args de la petición
        :param kwargs: conjunto de argumentos en formato dict de la petición
        :return: redirect
        """
        if request.user.is_authenticated and request.user.is_staff:
            pk = kwargs.get('id')
            domain = "{0}://{1}".format(request.scheme, request.get_host())
            query = get_object_or_404(Publication, id=pk)
            date_now = timezone.now()
            context = {
                'publication': query,
                'date_now': date_now,
                'domain': domain
            }
            # Se carga el template
            template = get_template(self.__get_template(query.category.certificate.template))
            html = template.render(context)
            # Se arma el nombre del path y el del archivo
            folder, file_name = self.__get_filepath(f'{query.category}')
            if not os.path.exists(folder):
                os.makedirs(folder)

            # Se arma la URL del archivo
            url_file = self.__get_url(f'{query.category}', file_name)
            full_file_path = folder + "/" + file_name
            write_to_file = open(full_file_path, "w+b")
            pisa.CreatePDF(html, dest=write_to_file)
            write_to_file.close()
            Certificate.objects.create(created_at=date_now, file_path=url_file, publication_id=pk)
            return redirect('/')
        else:
            return redirect('/')
