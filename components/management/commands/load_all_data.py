import json
import os
from django.core.management.base import BaseCommand
from components.models.ram import (
    RAM
)

DATA_DIR = 'data/'  # Carpeta donde pondrás tus archivos JSON

class Command(BaseCommand):
    help = 'Carga todos los componentes desde archivos JSON'

    def handle(self, *args, **kwargs):
        loaders = [
        
             ('ram.json', RAM, self.load_ram),
            
        ]

        for filename, model, loader in loaders:
            file_path = os.path.join(DATA_DIR, filename)
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    loader(data)
                    self.stdout.write(self.style.SUCCESS(f'Cargado: {filename} ({len(data)} registros)'))
            else:
                self.stdout.write(self.style.WARNING(f'Archivo no encontrado: {file_path}'))



    def load_ram(self, data):
        for item in data:
            RAM.objects.update_or_create(model=item['model'], defaults=item)

   
