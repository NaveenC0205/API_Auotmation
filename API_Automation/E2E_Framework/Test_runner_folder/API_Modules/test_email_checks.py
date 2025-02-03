import pytest
import csv
from pathlib import Path
from API_Automation.E2E_Framework.A_centrlized_file import api_ulits
from API_Automation.E2E_Framework.A_centrlized_file.api_ulits import validate_response_code
from API_Automation.E2E_Framework.base_config import Env, clients
from API_Automation.E2E_Framework.logger_config import logger

baseURLs = get_URL(Env, clients)

template_endpoint = "templates"
templates_using_id = "templates/{id}"


class TestEmailTemplates:

    @pytest.mark.order(1)
    def test_get_email_templates(self):
        all_templates = []

        for client_email in clients:
            baseURL = baseURLs.get(client_email)
            if not baseURL:
                pytest.fail(f"Base URL not found for client '{client_email}'")

            if client_email == 'email':
                url = f"{baseURL}/email/{template_endpoint}"
                logger.info(f"Sending GET request to: {url}")
                try:
                    response = api_ulits.getDATA(url)
                    validate_response_code(response, client_email)

                    response_data = response.json().get('data', [])
                    if response_data:
                        all_templates.extend(
                            [(template['id'], template['name'], template['data']) for template in response_data])

                        logger.info(f"All templates (id, name, data): {all_templates}")
                        return all_templates
                    else:
                        logger.warning("No templates found.")
                        return []
                except Exception as e:
                    logger.error(f"Error in test_get_email function: {e}")
                    pytest.fail(f"Test failed due to error: {e}")
                    break

    @pytest.mark.order(2)
    def test_get_template_by_id(self):
        all_template_data = []
        all_template_ids = []
        all_templates = self.test_get_email_templates()

        for template_id, template_name, template_data in all_templates:
            baseURL = baseURLs.get('email')
            if not baseURL:
                pytest.fail(f"Base URL not found for 'email'")

            url = f"{baseURL}/email/{templates_using_id.format(id=template_id)}"
            logger.info(f"Sending GET request to: {url}")
            try:
                response = api_ulits.getDATA(url)
                validate_response_code(response, 'email')
                response_data = response.json().get('data', {})

                if response_data:
                    logger.info(f"Validating template data for ID {template_id}...")
                    assert response_data.get(
                        'id') == template_id, f"Expected ID {template_id}, but got {response_data.get('id')}"
                    assert response_data.get(
                        'name') == template_name, f"Expected Name '{template_name}', but got {response_data.get('name')}"
                    assert response_data.get(
                        'data') == template_data, f"Expected Data '{template_data}', but got {response_data.get('data')}"

                    all_template_data.append(response_data)
                    all_template_ids.append(template_id)
                else:
                    logger.warning(f"No data found for template ID {template_id}.")
                    all_template_data.append({})
            except Exception as e:
                logger.error(f"Error in get_template_by_id function: {e}")
                pytest.fail(f"Test failed due to error: {e}")

        self.write_template_ids_to_csv(all_template_ids)
        return all_template_data

    def write_template_ids_to_csv(self, template_ids):
        home_directory = Path.home()
        output_dir = home_directory / 'pythonProject' / 'pythonProject' / 'Assignment' / 'edda29879786e996d997e8963c7c2435' / 'E2E_Framework' / 'Test_runner_folder' / 'Test_Data' / 'Template_ID'

        if not output_dir.exists() or not output_dir.is_dir():
            pytest.fail(f"The directory {output_dir} does not exist or is not a valid directory.")
        csv_file_path = output_dir / 'template_ids.csv'

        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Template ID'])  # Write header row
                for template_id in template_ids:
                    writer.writerow([template_id])

            logger.info(f"All template IDs have been written to {csv_file_path}.")
        except Exception as e:
            logger.error(f"Failed to write template IDs to CSV: {e}")
            pytest.fail(f"Test failed while writing template IDs to CSV: {e}")
