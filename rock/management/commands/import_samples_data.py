from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from rock.models import Mine, LithostratigraphicInfo, Erathem, System, Series, Formation, Member, RockSample, RockSampleName, RockSampleStructure
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
        parser.add_argument('--sample', action='store_true', help='导入样本信息')
        parser.add_argument('--delete', action='store_true', help='删除所有样本')

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

                        if RockSample.METHOD[0][1] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=RockSample.METHOD[0][1], header=None)
                            for i in range(13, sheet.shape[0], 19):
                                for j in range(0, 6):
                                    if i + j < sheet.shape[0]:
                                        name = sheet[1][i+j]
                                        if not pd.isna(name) and not RockSampleName.objects.filter(name=name).exists():
                                            print(name)
                                            inst = RockSampleName(name=name)
                                            inst.save()
                                            cnt += 1

                        if RockSample.METHOD[1][1] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=RockSample.METHOD[1][1], header=None)
                            for i in range(5, sheet.shape[0], 20):
                                for j in range(0, 15):
                                    if i + j < sheet.shape[0]:
                                        name = sheet[6][i+j]
                                        if not pd.isna(name) and not RockSampleName.objects.filter(name=name).exists():
                                            print(name)
                                            inst = RockSampleName(name=name)
                                            inst.save()
                                            cnt += 1

                        if RockSample.METHOD[2][1] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=RockSample.METHOD[2][1], header=None)
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
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        file_path = os.path.join(data_dir, file_name)
                        excel_file = pd.ExcelFile(file_path)
                        cnt = 0

                        for s in range(1, 3):
                            if RockSample.METHOD[s][1] in excel_file.sheet_names:
                                sheet = pd.read_excel(
                                    excel_file, sheet_name=RockSample.METHOD[s][1], header=None)
                                for i in range(5, sheet.shape[0]):
                                    name = sheet[4][i]
                                    if not pd.isna(name) and not '镜' in name and not '结构、构造' in name and not RockSampleStructure.objects.filter(name=name).exists():
                                        print(name)
                                        inst = RockSampleStructure(name=name)
                                        inst.save()
                                        cnt += 1

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully loaded {cnt} items from {file_name}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'{file_name}\t{e}'))
        elif options['delete']:
            RockSample.objects.all().delete()
        elif options['sample']:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        mine_num = Mine.objects.get(
                            name=file_name.split('.')[0].split('-')[-1])
                        file_path = os.path.join(data_dir, file_name)
                        excel_file = pd.ExcelFile(file_path)
                        cnt = 0

                        if RockSample.METHOD[0][1] in excel_file.sheet_names:
                            sheet = pd.read_excel(
                                excel_file, sheet_name=RockSample.METHOD[0][1], header=None)
                            method = RockSample.METHOD[0][0]
                            for i in range(13, sheet.shape[0], 19):
                                for j in range(0, 6):
                                    if i + j < sheet.shape[0] and not pd.isna(sheet[0][i+j-7]):
                                        analysis_number = sheet[0][i+j-7]
                                        number = sheet[1][i+j-7]
                                        depth = str(sheet[3][i+j-7])
                                        remarks = None
                                        if '-' in depth:
                                            remarks = depth.split('-')[-1]
                                            depth = float(depth.split('-')[0])
                                        name = RockSampleName.objects.get(
                                            name=sheet[1][i+j])
                                        description = sheet[3][i+j]
                                        if not RockSample.objects.filter(method=method, number=number).exists():
                                            inst = RockSample(method=method, mine_num=mine_num, analysis_number=analysis_number,
                                                              number=number, depth=depth, name=name, structure=None, description=description, remarks=remarks)
                                            inst.save()
                                            cnt += 1

                        for s in range(1, 3):
                            if RockSample.METHOD[s][1] in excel_file.sheet_names:
                                sheet = pd.read_excel(
                                    excel_file, sheet_name=RockSample.METHOD[s][1], header=None)
                                method = RockSample.METHOD[s][0]
                                for i in range(5, sheet.shape[0]):
                                    if not pd.isna(sheet[6][i]) and not '镜下岩石定名' in sheet[6][i]:
                                        analysis_number = sheet[0][i]
                                        number = sheet[1][i]
                                        depth = str(sheet[2][i])
                                        remarks = None
                                        if '-' in depth:
                                            remarks = depth.split('-')[-1]
                                            depth = float(depth.split('-')[0])
                                        structure = None
                                        if not pd.isna(sheet[4][i]):
                                            structure = RockSampleStructure.objects.get(
                                                name=sheet[4][i])
                                        description = sheet[5][i]
                                        name = RockSampleName.objects.get(
                                            name=sheet[6][i])
                                        if not RockSample.objects.filter(method=method, number=number).exists():
                                            inst = RockSample(method=method, mine_num=mine_num, analysis_number=analysis_number,
                                                              number=number, depth=depth, structure=structure, name=name, description=description, remarks=remarks)
                                            inst.save()
                                            cnt += 1

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully loaded {cnt} items from {file_name}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'{file_name}\t{e}'))
