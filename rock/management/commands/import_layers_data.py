from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from rock.models import Mine, LithostratigraphicInfo, Erathem, System, Series, Formation, Member
import pandas as pd
import numpy as np
import os


class Command(BaseCommand):
    help = 'Injecting lithostratigraphic units...'

    def add_arguments(self, parser):
        parser.add_argument('--unit', action='store_true', help='导入地质分层单元')
        parser.add_argument('--layer', action='store_true', help='导入地质分层信息')

    def handle(self, *args, **options):
        data_dir = os.path.join(
            settings.BASE_DIR, 'resource', 'rock_layers_data', 'stratification_data_sheet')
        if options['unit']:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        cnt = 0
                        file_path = os.path.join(data_dir, file_name)
                        data = pd.read_excel(file_path, sheet_name=0, header=2)

                        def save_unit(unit_class, unit_list, cnt):
                            for unit in unit_list:
                                if not pd.isna(unit) and not unit_class.objects.filter(name=unit).exists():
                                    inst = unit_class(name=unit)
                                    inst.save()
                                    cnt += 1
                            return cnt
                        try:
                            cnt = save_unit(Erathem, data['界'].tolist(), cnt)
                            cnt = save_unit(System, data['系'].tolist(), cnt)
                            cnt = save_unit(Series, data['统'].tolist(), cnt)
                            cnt = save_unit(Formation, data['组'].tolist(), cnt)
                            cnt = save_unit(Member, data['段'].tolist(), cnt)
                        except Exception as e:
                            self.stdout.write(str(e))

                        self.stdout.write(self.style.SUCCESS(
                            f'成功从"{file_name}"导入{cnt}个地质分层单元'))
                    except Exception as e:
                        self.stdout.write(f'{file_name}\t{e}')

        elif options['layer']:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        index = file_name.find('地层分层数据表')
                        if index == -1:
                            raise Exception('文件名不符合规范，导入失败')
                        else:
                            mine_num = Mine.objects.get(
                                name=file_name[:index])

                        file_path = os.path.join(data_dir, file_name)
                        data = pd.read_excel(file_path, sheet_name=0, header=2)
                        cnt = 0

                        for index, row in data.iterrows():
                            try:
                                erathem = None
                                system = None
                                series = None
                                formation = None
                                member = None
                                if not pd.isna(row['界']):
                                    erathem = Erathem.objects.get(
                                        name=row['界'])
                                if not pd.isna(row['系']):
                                    system = System.objects.get(
                                        name=row['系'])
                                if not pd.isna(row['统']):
                                    series = Series.objects.get(
                                        name=row['统'])
                                if not pd.isna(row['组']):
                                    formation = Formation.objects.get(
                                        name=row['组'])
                                if not pd.isna(row['段']):
                                    member = Member.objects.get(
                                        name=row['段'])
                                if pd.isna(row[5]) or pd.isna(row[6]):
                                    raise Exception('底深或厚度为空')
                                lower_border = row[5]
                                thickness = row[6]
                                higher_border = lower_border - thickness

                                if LithostratigraphicInfo.objects.filter(mine_num=mine_num, lower_border=lower_border).exists():
                                    raise Exception('地质分层信息重复')

                                inst = LithostratigraphicInfo(mine_num=mine_num, erathem=erathem, system=system, series=series, formation=formation,
                                                              member=member, lower_border=lower_border, higher_border=higher_border, thickness=thickness)
                                inst.save()
                                cnt += 1

                            except Exception as e:
                                self.stdout.write(self.style.ERROR(
                                    f'{file_name}:{index}\t{e}'
                                ))

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully loaded {cnt} items from {file_name}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'{file_name}\t{e}'))
