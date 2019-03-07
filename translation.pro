SOURCES         =	Settings/__init__.py \
                    Settings/settings.py \
                    Core/enums.py \
                    Core/DatabaseTools/__init__.py \
                    Core/DatabaseTools/SqlGenerator/SupportedDrivers/sqliteSqlGenerator.py \
                    Core/DatabaseTools/SqlGenerator/SupportedDrivers/__init__.py \
                    Core/DatabaseTools/SqlGenerator/sqlGeneratorFactory.py \
                    Core/DatabaseTools/SqlGenerator/__init__.py \
                    Core/DatabaseTools/SqlGenerator/abstractSqlGenerator.py \
                    Core/DatabaseTools/DatabaseManager/SupportedDrivers/sqliteDatabase.py \
                    Core/DatabaseTools/DatabaseManager/SupportedDrivers/__init__.py \
                    Core/DatabaseTools/DatabaseManager/abstractDatabase.py \
                    Core/DatabaseTools/DatabaseManager/__init__.py \
                    Core/DatabaseTools/DatabaseManager/databaseFactory.py \
                    Core/__init__.py \
                    Core/Sensor/sensor.py \
                    Core/Sensor/__init__.py \
                    Core/Sensor/sensorsManager.py \
                    Core/Terrain/terrain.py \
                    Core/Terrain/__init__.py \
                    Core/ProcessingTools/shooterFinder.py \
                    Core/ProcessingTools/__init__.py \
                    Core/ProcessingTools/rasterLayer.py \
                    Core/Shooter/__init__.py \
                    Core/Shooter/shooter.py \
                    Core/Observation/observation.py \
                    Core/Observation/__init__.py \
                    Core/Observation/observationsManager.py \
                    Gui/__init__.py \
                    Gui/CustomWidgets/PlottingWidgets/__init__.py \
                    Gui/CustomWidgets/PlottingWidgets/mayaViWidget.py \
                    Gui/CustomWidgets/__init__.py \
                    Gui/CustomWidgets/mainWindow.py \
                    Gui/CustomWidgets/summaryDialog.py \
                    Gui/CustomWidgets/sensorWidget.py \
                    Gui/CustomWidgets/observationWidget.py \
                    Gui/CustomWidgets/FeatureForms/observationsManagerDialog.py \
                    Gui/CustomWidgets/FeatureForms/__init__.py \
                    Gui/CustomWidgets/FeatureForms/featureForm.py \
                    Gui/guiManager.py \
                    resources.py \
                    main.py \
                    resources_rc.py

 FORMS          =	Gui/CustomWidgets/sensorWidget.ui \
                    Gui/CustomWidgets/mainWindow.ui \
                    Gui/CustomWidgets/summaryDialog.ui \
                    Gui/CustomWidgets/observationWidget.ui \
                    Gui/CustomWidgets/FeatureForms/featureForm.ui

 TRANSLATIONS   =   i18n/mopa_pt.ts

RESOURCES += resources.qrc \
             resources_rc.qrc