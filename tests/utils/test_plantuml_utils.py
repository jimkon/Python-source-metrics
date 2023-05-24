import unittest
from unittest.mock import patch, MagicMock

from pystruct.utils import plantuml_utils
from pystruct.utils.plantuml_utils import PlantUMLService,\
    PLANTUML_LOCAL_SERVER_URL, PLANTUML_WEB_SERVER_URL, PLANTUML_DOCKER_SERVER_URL


class TestPlantUMLService(unittest.TestCase):
    @patch.object(plantuml_utils.PlantUMLService, '__init__', return_value=None)
    def test_singleton(self, mock_init):
        p1, p2 = plantuml_utils.PlantUMLService.get_instance(), plantuml_utils.PlantUMLService.get_instance()
        self.assertTrue(p1 is p2)
        mock_init.assert_called_once()

    @patch('pystruct.utils.plantuml_utils.plantuml.PlantUML')
    def test_reset_plant_uml_server_local_success(self, mock_plantuml):
        mock_plant_uml_instance = MagicMock()
        mock_plantuml.return_value = mock_plant_uml_instance
        mock_plant_uml_instance.processes.return_value = 'Success'

        plant_uml_service = PlantUMLService()

        mock_plantuml.assert_called_with(PLANTUML_LOCAL_SERVER_URL)
        self.assertEqual(plant_uml_service._plant_uml_server, mock_plant_uml_instance)

    @patch('pystruct.utils.plantuml_utils.plantuml.PlantUML')
    def test_reset_plant_uml_server_local_fail_but_docker_success(self, mock_plantuml):
        def side_effect(url):
            if url == PLANTUML_LOCAL_SERVER_URL:
                raise plantuml_utils.plantuml.PlantUMLConnectionError()
            else:
                mock_plant_uml_instance = MagicMock()
                mock_plant_uml_instance.processes.return_value = 'Success'
                return mock_plant_uml_instance

        mock_plantuml.side_effect = side_effect

        plant_uml_service = PlantUMLService()

        mock_plantuml.assert_called_with(PLANTUML_DOCKER_SERVER_URL)
        self.assertEqual(plant_uml_service._plant_uml_server.processes(), 'Success')

    @patch('pystruct.utils.plantuml_utils.plantuml.PlantUML')
    def test_reset_plant_uml_server_local_and_docker_fail_but_WEB_success(self, mock_plantuml):
        def side_effect(url):
            if url == PLANTUML_LOCAL_SERVER_URL or url == PLANTUML_DOCKER_SERVER_URL:
                raise plantuml_utils.plantuml.PlantUMLConnectionError()
            else:
                mock_plant_uml_instance = MagicMock()
                mock_plant_uml_instance.processes.return_value = 'Success'
                return mock_plant_uml_instance

        mock_plantuml.side_effect = side_effect

        plant_uml_service = PlantUMLService()

        mock_plantuml.assert_called_with(PLANTUML_WEB_SERVER_URL)
        self.assertEqual(plant_uml_service._plant_uml_server.processes(), 'Success')


    @patch('pystruct.utils.plantuml_utils.plantuml.PlantUML')
    def test_reset_plant_uml_server_local_and_web_connection_error(self, mock_plantuml):
        mock_plantuml.side_effect = plantuml_utils.plantuml.PlantUMLConnectionError()

        with self.assertRaises(plantuml_utils.plantuml.PlantUMLConnectionError):
            plant_uml_service = PlantUMLService()

            mock_plantuml.assert_called_with(PLANTUML_LOCAL_SERVER_URL)
            mock_plantuml.assert_called_with(PLANTUML_WEB_SERVER_URL)
            self.assertIsNone(plant_uml_service._plant_uml_server)


if __name__ == '__main__':
    unittest.main()
