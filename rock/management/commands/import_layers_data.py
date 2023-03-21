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

    def handle(self, *args, **options):
        data_dir = os.path.join(
            settings.BASE_DIR, 'resource', 'rock_layers_data')
        if options['unit']:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        file_path = os.path.join(data_dir, file_name)
                        data = pd.read_excel(file_path, sheet_name=0, header=2)

                        def save_unit(unit_class, unit_list):
                            for unit in unit_list:
                                if not unit_class.objects.filter(name=unit).exists():
                                    inst = unit_class(name=unit)
                                    inst.save()
                        try:
                            save_unit(Erathem, data['界'].tolist())
                            save_unit(System, data['系'].tolist())
                            save_unit(Series, data['统'].tolist())
                            save_unit(Formation, data['组'].tolist())
                            save_unit(Member, data['段'].tolist())
                        except Exception:
                            self.stdout.write(Exception)

                        self.stdout.write(self.style.SUCCESS(
                            f'成功从"{file_name}"导入地质分层单元'))
                    except Exception:
                        self.stdout.write(Exception)
        else:
            for file_name in os.listdir(data_dir):
                if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    try:
                        index = file_name.find('地层分层数据表')
                        if index == -1:
                            raise Exception('"{file_name}"\t文件名不符合规范，导入失败')
                        else:
                            mine_inst = Mine.objects.get(
                                name=file_name[:index])

                        file_path = os.path.join(data_dir, file_name)
                        data = pd.read_excel(file_path, sheet_name=0, header=2)

                        for index, row in data.iterrows():
                            try:
                                erathem = row['界']
                                system = row['系']
                                series = row['统']
                                formation = row['组']
                                member = row['段']
                                if pd.isna(row[5]) or pd.isna(row[6]):
                                    raise Exception(
                                        '{file_name}:{index}\t底深或厚度为空')
                                lower_border = row[5]
                                thickness = row[6]
                                higher_border = lower_border - thickness

                                inst = LithostratigraphicInfo(erathem=erathem, system=system, series=series, formation=formation,
                                                              member=member, lower_border=lower_border, higher_border=higher_border, thickness=thickness)

                            except Exception:
                                self.stdout.write(Exception)

                        self.stdout.write(self.style.SUCCESS(
                            f'Successfully loaded data from {file_name}'))
                    except Mine.DoesNotExist:
                        self.stdout.write(Mine.DoesNotExist)
                    except Exception:
                        self.stdout.write(Exception)
