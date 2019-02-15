SOURCES         =	Settings/settings.py \
                    Settings/__init__.py \
                    Gui/CustomWidgets/mainWindow.py \
                    Gui/CustomWidgets/PlottingWidgets/mayaViWidget.py \
                    Gui/CustomWidgets/PlottingWidgets/__init__.py \
                    Gui/CustomWidgets/summaryDialog.py \
                    Gui/CustomWidgets/__init__.py \
                    Gui/__init__.py \
                    Gui/guiManager.py \
                    tests.py \
                    main.py \
                    resources.py \
                    resources_rc.py \
                    .dev/originalScript.py \
                    Core/ProcessingTools/rasterLayer.py \
                    Core/ProcessingTools/__init__.py \
                    Core/ProcessingTools/shooterFinder.py \
                    Core/Sensor/sensorsManager.py \
                    Core/Sensor/__init__.py \
                    Core/Sensor/sensor.py \
                    Core/DatabaseTools/SqlGenerator/abstractSqlGenerator.py \
                    Core/DatabaseTools/SqlGenerator/SupportedDrivers/__init__.py \
                    Core/DatabaseTools/SqlGenerator/SupportedDrivers/sqliteSqlGenerator.py \
                    Core/DatabaseTools/SqlGenerator/__init__.py \
                    Core/DatabaseTools/SqlGenerator/sqlGeneratorFactory.py \
                    Core/DatabaseTools/__init__.py \
                    Core/DatabaseTools/DatabaseManager/SupportedDrivers/sqliteDatabase.py \
                    Core/DatabaseTools/DatabaseManager/SupportedDrivers/__init__.py \
                    Core/DatabaseTools/DatabaseManager/__init__.py \
                    Core/DatabaseTools/DatabaseManager/abstractDatabase.py \
                    Core/DatabaseTools/DatabaseManager/databaseFactory.py \
                    Core/Shooter/__init__.py \
                    Core/Shooter/shooter.py \
                    Core/enums.py \
                    Core/Terrain/__init__.py \
                    Core/Terrain/terrain.py \
                    Core/__init__.py \
                    Core/Observation/observationsManager.py \
                    Core/Observation/observation.py \
                    Core/Observation/__init__.py

 FORMS         =	Gui/CustomWidgets/summaryDialog.ui \
                    Gui/CustomWidgets/mainWindow.ui

 TRANSLATIONS    = i18n/mopa_pt.ts

RESOURCES += resources.qrc