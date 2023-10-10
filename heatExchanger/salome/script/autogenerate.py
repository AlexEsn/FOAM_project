import salome
salome.salome_init()
import SMESH
from salome.geom import geomBuilder
from salome.smesh import smeshBuilder

geom_builder = geomBuilder.New()
smesh_builder = smeshBuilder.New()

# Создание нагревателя (heater)
heater_length = 100
heater_width = 20
heater_height = 10
heater = geom_builder.MakeBox(-heater_length/2, -heater_width/2, 0, heater_length/2, heater_width/2, heater_height)

# Создание радиатора (fin)
fin_length = 150
fin_width = 30
fin_height = 15
fin = geom_builder.MakeBox(-fin_length/2, -fin_width/2, heater_height, fin_length/2, fin_width/2, heater_height + fin_height)

# Создание воздуховода (duct)
duct_length = 200
duct_width = 100
duct_height = 50
duct = geom_builder.MakeBox(-duct_length/2, -duct_width/2, heater_height + fin_height, duct_length/2, duct_width/2, heater_height + fin_height + duct_height)

# Объединение всех частей
assembly = geom_builder.MakeFuse(heater, fin)
assembly = geom_builder.MakeFuse(assembly, duct)

# Добавление в геометрическую модель
geom_builder.addToStudy(heater, "Heater")
geom_builder.addToStudy(fin, "Fin")
geom_builder.addToStudy(duct, "Duct")
geom_builder.addToStudy(assembly, "Assembly")

# Создание группы для всех частей
all_parts_group = geom_builder.CreateGroup(assembly, geom_builder.ShapeType["SOLID"])
all_parts_group.SetName("All_Parts_Group")
geom_builder.addToStudy(all_parts_group, "All Parts")

# Создание групп для каждой части отдельно
heater_group = geom_builder.CreateGroup(heater, geom_builder.ShapeType["SOLID"])
heater_group.SetName("Heater_Group")
geom_builder.addToStudy(heater_group, "Heater Group")

fin_group = geom_builder.CreateGroup(fin, geom_builder.ShapeType["SOLID"])
fin_group.SetName("Fin_Group")
geom_builder.addToStudy(fin_group, "Fin Group")

duct_group = geom_builder.CreateGroup(duct, geom_builder.ShapeType["SOLID"])
duct_group.SetName("Duct_Group")
geom_builder.addToStudy(duct_group, "Duct Group")

# Создание сетки для геометрии, если необходимо
# Вам нужно будет добавить код для создания сетки в соответствии с вашими требованиями

# Сохранение проекта
# salome.myStudyManager.SaveAs("my_model")

# Завершение работы с Salome
# salome.salome_close()
