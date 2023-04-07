from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from rock.models import Mine, LithostratigraphicInfo, Erathem, System, Series, Formation, Member, RockSampleName
import pandas as pd
import numpy as np
import os


class Command(BaseCommand):
    help = 'Injecting rock samples data...'
    SHEET_NAMES = ['碎屑岩', '岩浆岩', '井壁取心']

    def add_arguments(self, parser):
        parser.add_argument('--name', action='store_true', help='导入镜下命名')
        parser.add_argument(
            '--structure', action='store_true', help='导入结构')

    def handle(self, *args, **options):
        data_dir = os.path.join(
            settings.BASE_DIR, 'resource', 'rock_layers_data', 'rock_sample_sheet')
        if options['name']:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        file_path = os.path.join(data_dir, file_name)
                        excel_file = pd.ExcelFile(file_path)
                        cnt = 0

                        if self.SHEET_NAMES[0] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=self.SHEET_NAMES[0], header=None)
                            for i in range(13, sheet.shape[0], 19):
                                for j in range(0, 6):
                                    if i + j < sheet.shape[0]:
                                        name = sheet[1][i+j]
                                        if not pd.isna(name) and not RockSampleName.objects.filter(name=name).exists():
                                            print(name)
                                            inst = RockSampleName(name=name)
                                            inst.save()
                                            cnt += 1

                        if self.SHEET_NAMES[1] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=self.SHEET_NAMES[1], header=None)
                            for i in range(5, sheet.shape[0], 20):
                                for j in range(0, 15):
                                    if i + j < sheet.shape[0]:
                                        name = sheet[6][i+j]
                                        if not pd.isna(name) and not RockSampleName.objects.filter(name=name).exists():
                                            print(name)
                                            inst = RockSampleName(name=name)
                                            inst.save()
                                            cnt += 1

                        if self.SHEET_NAMES[2] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=self.SHEET_NAMES[2], header=None)
                            for i in range(5, sheet.shape[0]):
                                name = sheet[6][i]
                                if not pd.isna(name) and not '镜下岩石定名' in name and not RockSampleName.objects.filter(name=name).exists():
                                    print(name)
                                    inst = RockSampleName(name=name)
                                    inst.save()
                                    cnt += 1

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully loaded {cnt} items from {file_name}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'{file_name}\t{e}'))
        elif options['structure']:
            pass
        else:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        cnt = 0
                        file_path = os.path.join(data_dir, file_name)
                        mine_num = Mine.objects.get(
                            name=file_name.split('.')[0].split('-')[-1])

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'{file_name}\t{e}'))
