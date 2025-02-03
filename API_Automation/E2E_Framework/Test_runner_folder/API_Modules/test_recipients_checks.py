import pytest
import csv
from pathlib import Path
from API_Automation.E2E_Framework.A_centrlized_file import api_ulits
from API_Automation.E2E_Framework.A_centrlized_file.api_ulits import validate_response_code
from API_Automation.E2E_Framework.base_config import Env, clients
from API_Automation.E2E_Framework.logger_config import logger

baseURLs = get_URL(Env, clients)
recipients_endpoint = "lists"
recipients_using_id = "lists/{id}"


class TestRecipients:

    @pytest.mark.order(3)
    def test_get_recipients_list(self):
        all_recipient_data = []

        for client_recipients in clients:
            baseURL = baseURLs.get(client_recipients)
            if not baseURL:
                pytest.fail(f"Base URL not found for client '{client_recipients}'")

            if client_recipients == 'recipients':
                url = f"{baseURL}/recipients/{recipients_endpoint}"
                logger.info(f"Sending GET request to: {url}")

                try:
                    response = api_ulits.getDATA(url)
                    validate_response_code(response, client_recipients)
                    response_data = response.json().get('data', [])

                    all_recipient_data = [
                        (recipient_list['id'], recipient['id'], recipient['email'])
                        for recipient_list in response_data
                        for recipient in recipient_list.get('recipients', [])
                    ]

                    if all_recipient_data:
                        logger.info(f"All recipient data (list_id, recipient_id, email): {all_recipient_data}")
                        return all_recipient_data
                    else:
                        logger.warning("No recipient lists found.")
                        return []

                except Exception as e:
                    logger.error(f"Error in test_get_email_templates function: {e}")
                    pytest.fail(f"Test failed due to error: {e}")

    @pytest.mark.order(4)
    def test_get_recipient_by_id(self):
        all_recipient_list_ids = set()
        all_recipient_lists = self.test_get_recipients_list()

        if not isinstance(all_recipient_lists, list):
            pytest.fail("test_get_email_templates() did not return a list.")

        for recipient_list in all_recipient_lists:
            if len(recipient_list) < 3:
                logger.warning(f"Skipping invalid recipient list data: {recipient_list}")
                continue

            recipient_list_id, recipient_list_name, recipient_email = recipient_list
            baseURL = baseURLs.get('recipients')

            if not baseURL:
                pytest.fail(f"Base URL not found for 'recipients'")

            if not isinstance(recipients_using_id, str) or "{id}" not in recipients_using_id:
                pytest.fail("Invalid format for `recipients_using_id`")

            url = f"{baseURL}/recipients/{recipients_using_id.format(id=recipient_list_id)}"
            logger.info(f"Sending GET request to: {url}")

            try:
                response = api_ulits.getDATA(url)
                validate_response_code(response, 'recipients')
                response_data = response.json().get('data', {})

                if response_data:
                    all_recipient_list_ids.add(recipient_list_id)

                    logger.info(f"Validated recipient list ID: {recipient_list_id}")
                else:
                    logger.warning(f"No data found for recipient list ID {recipient_list_id}.")

            except Exception as e:
                logger.error(f"Error in get_recipient_by_id function: {e}")
                pytest.fail(f"Test failed due to error: {e}")

        self.write_recipient_list_ids_to_csv(all_recipient_list_ids)
        return list(all_recipient_list_ids)

    def write_recipient_list_ids_to_csv(self, recipient_list_ids):
        home_directory = Path.home()
        output_dir = home_directory / 'pythonProject' / 'pythonProject' / 'Assignment' / 'edda29879786e996d997e8963c7c2435' / 'E2E_Framework' / 'Test_runner_folder' / 'Test_Data' / 'Recipients_ID'

        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            pytest.fail(f"Failed to create directory {output_dir}: {e}")

        csv_file_path = output_dir / 'recipient_list_ids.csv'

        try:
            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Recipient List ID'])

                for recipient_list_id in recipient_list_ids:
                    writer.writerow([recipient_list_id])

            logger.info(f"All recipient list IDs have been written to {csv_file_path}.")
        except Exception as e:
            logger.error(f"Failed to write recipient list IDs to CSV: {e}")
            pytest.fail(f"Test failed while writing recipient list IDs to CSV: {e}")
